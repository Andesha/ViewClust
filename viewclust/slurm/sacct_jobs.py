from io import StringIO
import subprocess
import pandas as pd
import os

# Time columns in job records
# If we exclude PENDING jobs (that we do in slurm_raw_processing), all time columns should have a time stamp,
# except RUNNING jobs that do not have the 'End' stamp.
time_columns = ['Eligible','Submit','Start','End']

# Define what constitutes a duplicate job
duplicate_job_def = ['JobID','Submit','Start']


def sacct_jobs(account_query, d_from, d_to='', debugging=False,
               serialize_frame='', slurm_names=False):
    """Ingest job record information from slurm via sacct and return DataFrame.

    Parameters
    -------
    account_query: str
        String query to be sent to sacct via -A flag.
    d_from: date str
        Beginning of the query period, e.g. '2019-04-01T00:00:00
    debugging: boolean, optional
        Boolean for reporting progress to stdout. Default False.
    sacct_file: str, optional
        Loads a raw query from file.
        If empty, query is rerun. Defaults to the empty string.
    serialize_frame: str, optional
        Pickle the resulting DataFrame.
        If empty, pickling is skipped. Defaults to the empty string.
    slurm_names: str, optional
        Keep slurm's sacct column names instead of shorthands.
        Defaults to False.

    Returns
    -------
    DataFrame
        Returns a standard pandas DataFrame, or an empty dataframe if no
        jobs are found.
    """

    raw_frame = _get_slurm_records(pd.to_datetime(d_from))
    out_frame = _slurm_raw_processing(raw_frame, slurm_names)

    # Legacy/consistency check:
    # Protect end time for jobs that are still currently running
    out_frame['end'] = out_frame['end'].replace({pd.NaT: pd.to_datetime(d_to)})

    # return _slurm_consistency_check(out_frame) if debugging else out_frame
    # TODO: consisder swapping this to a better format
    if serialize_frame != '':
        out_frame.to_pickle(serialize_frame, protocol=4)
    return out_frame


def _get_slurm_records(arg, ssh_client=None):
    '''Retrieve records either via SSH or from a file.'''

    sacct_format = 'Account,AllocCPUS,AllocNodes,AllocTRES,AssocID,Cluster,CPUTimeRAW,'\
    'CPUTime,DerivedExitCode,ElapsedRaw,Elapsed,Eligible,End,ExitCode,Flags,GID,Group,'\
    'JobID,JobIDRaw,NCPUS,NNodes,NodeList,Priority,Partition,QOS,QOSRAW,Reason,ReqCPUS,'\
    'ReqMem,ReqNodes,ReqTRES,Reserved,ResvCPURAW,ResvCPU,Start,State,Submit,Suspended,'\
    'SystemCPU,TimelimitRaw,Timelimit,TotalCPU,UID,User,UserCPU,WorkDir'
    sacct_command = 'TZ=UTC sacct'
    sacct_options = f'--duplicates --allusers --allocations --parsable2 --delimiter=";" --format={sacct_format}'

    if isinstance(arg, str):
        # Read a SLURM dump from a file
        source = arg
        command = None
        if not os.path.isfile(source):
            print('The seed file does not exist. Quitting.')
            return pd.DataFrame()
    elif isinstance(arg, list) and arg:
        # Get specific jobs
        command = f'{sacct_command} {sacct_options} --jobs {",".join(arg)}'
    elif isinstance(arg, pd.Timestamp):
        # Get a list of jobs in a date range
        # Note that --start selects jobs in ANY state after the specified time.
        # This is not the same as filtering by 'Start' afterwards.
        command = f'{sacct_command} {sacct_options} --start {arg:%Y-%m-%dT%H:%M} --end Now\n'
    else:
        print('Unexpected input parameter to get_slurm_records().')
        return pd.DataFrame()

    if command:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        source = stdout.decode('UTF-8')

    try:
        records = pd.read_csv(StringIO(source), sep=';', dtype='str', on_bad_lines='skip')
    except e:  # TODO: Fix this to be less heavy handed
        return pd.DataFrame()

    return pd.DataFrame() if records.empty else records


def _slurm_raw_processing(records, slurm_names):

    check = records.duplicated( keep=False )
    if check.any():
        duplicated_records = records.loc[ check, 'JobID'].unique().tolist()
        len1 = len(records)
        records.drop_duplicates( keep='last', inplace=True, ignore_index=True )
        len2 = len(records)
        print(f'Dropped {len1-len2} fully identical records.')

    # Convert date/times columns from 'str' to the 'datetime' type.
    # Invalid parsing will be set to NaN.
    records[time_columns] = records[time_columns].apply( pd.to_datetime, errors='coerce' )

    # Convert integer columns from 'str' to 'int64'
    # Invalid parsing will be set to NaN and then to 0
    columns_int = ['AllocCPUS', 'AllocNodes', 'AssocID', 'CPUTimeRAW', 'ElapsedRaw', 'GID', 'JobIDRaw',
    'NCPUS', 'NNodes', 'Priority', 'QOSRAW', 'ReqCPUS', 'ReqNodes', 'ResvCPURAW', 'TimelimitRaw', 'UID']
    records[columns_int] = records[columns_int].apply( pd.to_numeric, errors='coerce' ).fillna(0).astype('Int64')

    # Replace unnecessary columns
    records['Timelimit'] = records['TimelimitRaw']
    records['CPUTime'] = records['CPUTimeRAW']
    records['Elapsed'] = records['ElapsedRaw']
    records['ResvCPU'] = records['ResvCPURAW']
    records.drop( columns=['TimelimitRaw','CPUTimeRAW','ElapsedRaw','ResvCPURAW'], inplace=True )

    # Allocated memory per job. Note that memory can be specified as a float in the submission script,
    # therefore we preserve this type for multiplication, but then cast to integer.
    records[['Mem','_mem_unit']] = records['AllocTRES'].str.extract('mem=([0-9.]+)(M|G|T)')
    records['Mem'] = pd.to_numeric( records['Mem'], errors='coerce').fillna(0).astype('float64')
    records['Mem'].mask( records['_mem_unit']=='G', records['Mem']*1024, inplace=True )
    records['Mem'].mask( records['_mem_unit']=='T', records['Mem']*1024*1024, inplace=True )
    records['Mem'] = records['Mem'].round(0).astype('Int64')
    records['MemTime'] = records['Mem']*records['Elapsed']
    records.drop( columns=['_mem_unit'], inplace=True )

    # GPUs: Get a number of allocated GPUs and GPU-seconds
    records['NGPUS'] = records['AllocTRES'].str.extract('gpu=(\d+)',expand=False)
    records['NGPUS'] = pd.to_numeric( records['NGPUS'], errors='coerce' ).fillna(0).astype('Int64')
    records['GPUTime'] = records['NGPUS']*records['Elapsed']

    if not slurm_names:
        old_fields = ['jobid', 'user', 'account', 'submit', 'start', 'end', 'ncpus', 'nnodes',
        'reqmem', 'timelimit', 'state', 'reqtres', 'reqtres', 'priority',
        'partition', 'reqcpus', 'mem', 'ngpus', 'alloctres']

        records.columns = records.columns.str.lower()
        records = records.drop(records.columns.difference(old_fields), 1)

    return records

def _slurm_consistency_check( records ):
    '''
    Perform consistency checks of the SLURM records.
    '''
    print('Consistency check started.')

    # Exclude running and pending jobs from analysis
    states = ['RUNNING','PENDING']
    check = records['State'].isin( states )
    if any(check):
        print(f'  {sum(check)} records of jobs in {states} states have been excluded from the consistency check.')
        records = records[ ~check ]

    # Runaway jobs
    # Some 'FAILED' records might have NaN in 'End' due to SLURM glitches. These are called runaway jobs.
    # They can be fixed by running 'sacctmgr show RunawayJobs' on the cluster.
    # We also check all other time columns just in case.
    check = records[ time_columns ].isna().any(1)
    if any(check):
        print(f'  NaNs detected in columns {time_columns} in the following {sum(check)} records that have been excluded: {records.loc[check,"JobID"].to_list()}')
        records = records[ ~check ]

    # Data consistency checks
    # Verify that 'End'-'Start' is equal to 'Elapsed'
    check = ( (records['End']-records['Start']).dt.total_seconds().astype('int64') - records['Elapsed'] )!=0
    if any(check):
        print(f'  Failed consistency check for Elapsed on the following {sum(check)} JobIDs:', records.loc[check,'JobID'].to_list() )

    # Verify that 'NCPUS'*'Elapsed' is equal to 'CPUTime'
    check = ( records['NCPUS']*records['Elapsed'] - records['CPUTime'] )!=0
    if any(check):
        print(f'  Failed consistency check for CPUTime on the following {sum(check)} JobIDs:', records.loc[check,'JobID'].to_list() )

    # Verify that 'AllocCPUS' and 'NCPUS' are the same (per SLURM documentation).
    check = ( records['AllocCPUS']!=records['NCPUS'] )
    if any(check):
        print(f'  Failed consistency check for AllocCPUS and NCPUS on the following {sum(check)} JobIDs:', records.loc[check,'JobID'].to_list() )

    print('Consistency check ended.')

    return records
