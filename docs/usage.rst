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
