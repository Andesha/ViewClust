=====
Usage
=====

To use **ViewClust** in a project::

    import viewclust

* All following examples are using ``vc`` as an alias::

    import viewclust as vc

* Functions can then be called with ``vc``::

    vc.job_use(jobs, d_from, target)

To use the **ViewClust/Slurm** `sub-module <https://github.com/Andesha/ViewClust/tree/master/viewclust/slurm>`_::

    from viewclust import slurm

* Functions can then be called with ``slurm``::

    slurm.sacct_jobs(account, d_from, d_to=d_to)

ViewClust has the following collection of functions:

* ``get_users_run`` (see `docstring <https://github.com/Andesha/ViewClust/blob/master/viewclust/get_users_run.py>`_)
* ``job_use`` (see `docstring <https://github.com/Andesha/ViewClust/blob/master/viewclust/job_use.py>`_)
* ``node_use`` (see `docstring <https://github.com/Andesha/ViewClust/blob/master/viewclust/node_use.py>`_)
* ``slurm.mem_info`` (see `docstring <https://github.com/Andesha/ViewClust/blob/master/viewclust/slurm/mem_info.py>`_)
* ``slurm.sacct_jobs`` (see `docstring <https://github.com/Andesha/ViewClust/blob/master/viewclust/slurm/sacct_jobs.py>`_)


Investigating Core-year Usage
########

The following pattern can be used to process jobs dataframes and get instantaneous core-year usage::

    import viewclust as vc
    from viewclust import slurm

    # Query parameters
    account = 'def-tk11br_cpu'
    d_from = '2021-02-14T00:00:00'
    d_to = '2021-03-16T00:00:00'

    # DataFrame query
    jobs_df = slurm.sacct_jobs(account, d_from, d_to=d_to)

    # ViewClust processing
    target = 50
    clust_target, queued, running, dist = vc.job_use(jobs_df, d_from, target, d_to=d_to, use_unit='cpu-eqv')

Things to note about this example:

* The functions use optional arguments. Docstrings are supported in all cases.
* To generate the input jobs dataframe, we are using an included ``slurm`` helper function.

  * The main job query from Slurm can take a long time if your query period is large!

* Input frames can be anything as long as they are dataframes with the expected columns:

  * ``submit`` (``datetime64[ns]``): submit time
  * ``start`` (``datetime64[ns]``): start time
  * ``end`` (``datetime64[ns]``): end time
  * ``state`` (String or ``object``): job state
  * ``timelimit`` (``timedelta64[ns]``): reserved run time
  * ``reqcpus`` (``int64``): total number of CPU cores
  * ``mem`` (``int64``): total reserved memory
  * ``reqtres`` (String or ``object``): all requested resources, including GPUs

* A plot can be generated with `ViewClust-Vis <https://viewclust-vis.readthedocs.io/en/latest/usage.html>`_

Investigating Memory Usage
########

In an effort to help with tickets, the follow pattern can be used to investigate memeory efficiency::

    import viewclust as vc
    import pandas as pd
    from viewclust import slurm

    # Define some accounts to look at
    accounts = ['def-tk11br_cpu','def-jdesjard_cpu']

    # Pick a time to start looking from
    d_from = '2020-01-10T00:00:00'

    # Loop over your queries if you want
    for account in accounts:
        print('Working on: ', account) # Just some printing to make sure things are running
        # Queries slurm and uses viewclust to build memory usage plots via
        # MaxRSS field inside of sacct.
        slurm.mem_info(d_from, account, fig_out=account+'.html')
        # Saves output as an html figure!

Things to note about this example:

* The functions use optional arguments. Docstrings are supported in all cases.
* To generate the input job frame, we are using an included slurm helper function
* Data is based on MaxRSS from slurm - which isn't always a clear indicator

Generating a RAC Summary
########

This example script is a sample of what could be used to generate a RAC summary.
Input in this case is a csv file of the following form: account,core_award,core_eqv_award.

The example is provided with comments describing what could be changed here::

    # This script is meant to be run via:
    # python rac_summary.py

    import pandas as pd
    import viewclust as vc
    from viewclust import slurm

    # The purpose of this script is to iterate over a file of accounts and
    # compute usage summaries for each account as well as generate a helper reference page.
    # Typically would be used as a base structure for iterating over RACs.
    # For more specific usage, consult docstrings of functions.

    # Query information
    d_from = '2019-10-01T00:00:00'
    d_to = '2019-12-31T00:00:00'
    account_file = 'test_accounts.csv' # of the form: account, core, ceqv

    # Read file, assuming headers
    account_frame = pd.read_csv(account_file)

    # Holders for summary generation
    dist_list = []
    account_list = []

    # Not the most quick, but fine for small scale
    for _, entry in account_frame.iterrows():
        # Just some quick checking if the account info makes sense
        # Probably a better way to do this...
        account = entry['account']
        if not account.endswith('_cpu'):
            print('Missing cpu or gpu account suffix. Assuming cpu.')
            account += '_cpu'

        # Extract target
        target = entry['ceqv']

        # Perform sacct query
        job_frame = slurm.sacct_jobs(account, d_from, d_to=d_to)
        # Make sure there's actually jobs
        if job_frame is not None:
            # Compute usage in terms of core equiv
            clust_target, queued, running, dist = vc.job_use(job_frame, d_from, target, d_to=d_to, use_unit='cpu-eqv')
            insta_plot(clust_target, queued, running, fig_out=account+'.html'):

            # Hand information off to lists for later if need be
            account_list.append(account)
            dist_list.append(dist)
            print('Done account: ', account)
        else:
            # Potentially handle differently, but skip for now
            print('Skipped account: ', account)

Things to note about this example:

* The functions use optional arguments. Docstrings are supported in all cases.
* To generate the input job frame, we are using an included slurm helper function
