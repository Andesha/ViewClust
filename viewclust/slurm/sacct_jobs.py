import subprocess
from datetime import datetime
import pandas as pd

def sacct_jobs(account_query, d_from, d_to='', debugging=False,
               write_txt='', sacct_file='', serialize_frame=''):
    """Ingest job record information from slurm via sacct and return DataFrame.

    Parameters
    -------
    account_query: str
        String query to be sent to sacct via -A flag.
    d_from: date str
        Beginning of the query period, e.g. '2019-04-01T00:00:00'
    d_to: optional, date str
        End of the query period, e.g. '2020-01-01T00:00:00' Defaults to now if empty.
    debugging: boolean, optional
        Boolean for reporting progress to stdout. Default False.
    write_txt: str, optional
        Writes the results of the raw sacct query to given file.
        If empty, no file is created. Defaults to the empty string.
    sacct_file: str, optional
        Loads a raw query from file. If empty, query is rerun. Defaults to the empty string.
    serialize_frame: str, optional
        Pickle the resulting DataFrame. If empty, pickling is skipped. Defaults to the empty string.

    Returns
    -------
    DataFrame
        Returns a standard pandas DataFrame, or None if no jobs found.
    """

    # d_to boilerplate
    if d_to == '':
        now = datetime.now()
        d_to = now.strftime('%Y-%m-%dT%H:%M:%S')

    headers = ['jobid', 'user', 'account', 'submit', 'start', 'end',
               'ncpus', 'nnodes', 'reqmem', 'timelimit', 'state',
               'reqgres', 'priority', 'partition']
    data = ''

    if sacct_file == '':
        base_cmd = ['sacct', '-aX', '-A', account_query, '-S', d_from, '-E', d_to,
                    '-p', '--delimiter', '"|"', '-n', '--units=M']
        base_cmd.append('-o')
        base_cmd.append(','.join(headers)+'%36')

        data = subprocess.check_output(base_cmd).decode('UTF-8')

        if write_txt != '':
            with open(write_txt, 'w') as f_id:
                f_id.write('%s' % data)
    else:
        with open(sacct_file, 'r') as f_id:
            data = f_id.read()

    if debugging:
        print('Done sacct query')

    job_frame = pd.DataFrame([x.split('"|"') for x in data.split('\n')])
    # Below two drops are tested for both loading from file and raw string loading
    job_frame = job_frame.iloc[:, :-1] # Due to split implementation...
    job_frame = job_frame.iloc[:-1, :] # Due to split implementation...

    # Edge case before things start to happen...
    if job_frame.empty:
        return None

    job_frame.columns = headers

    # Below calls are in an effort to align sacct to elasticsearch implementation
    job_frame['reqcpus'] = pd.to_numeric(job_frame['ncpus'])
    job_frame['nnodes'] = pd.to_numeric(job_frame['nnodes'])
    job_frame['submit'] = pd.to_datetime(job_frame['submit'])
    job_frame['start'] = pd.to_datetime(job_frame['start'], errors='coerce')
    job_frame['end'] = pd.to_datetime(job_frame['end'], errors='coerce')

    # Fix jobs with day limits and convert to timedelta
    job_frame.update(job_frame.timelimit.loc[lambda x: x.str.contains('-')] \
                     .str.replace('-', ' days '))
    job_frame['timelimit'] = pd.to_timedelta(job_frame['timelimit'])

    # Protect end time for jobs that are still currently running
    job_frame['end'] = job_frame['end'].replace({pd.NaT: pd.to_datetime(d_to)})

    # Construct mem column
    job_frame['memHold'] = job_frame['reqmem'].map(lambda x: int(x.lstrip('+-').rstrip('MmNnCc')))
    core_mask = (job_frame['reqmem'].str.contains('c'))
    node_mask = (job_frame['reqmem'].str.contains('n'))
    job_frame.loc[core_mask, 'memHold'] = (job_frame['reqcpus'] * job_frame['memHold'])
    job_frame.loc[node_mask, 'memHold'] = (job_frame['nnodes'] * job_frame['memHold'])
    job_frame = job_frame.rename(columns={'memHold':'mem'})

    if debugging:
        print(job_frame)

    if serialize_frame != '':
        job_frame.to_pickle(serialize_frame)

    if debugging:
        print('Done sacctJobs.py')

    return job_frame
