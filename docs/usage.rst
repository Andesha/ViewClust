=====
Usage
=====

To use ViewClust in a project::

    import viewclust

Or use an alias::

    import viewclust as vc

Functions can then be called as expected via::

    vc.job_stack(jobs)

Generating Job Stack Plots
########

To view a job stack plot for an account group the following pattern can be used::

    import viewclust as vc
    from viewclust import slurm

    # Query parameters
    d_from = '2020-01-01T00:00:00'
    d_to = '2020-02-02T00:00:00'
    account = 'def-tk11br_cpu'

    # More parameters and default arguments explored in docstrings
    job_frame = slurm.sacct_jobs(account, d_from, d_to=d_to)

    # Can take some time...
    print('Computing job stack...')
    vc.job_stack(job_frame, fig_out=account+'_stack.html', plot_title=account)

Things to note about this example:

* The functions use optional arguments. Docstrings are supported in all cases.
* To generate the input job frame, we are using an included slurm helper function
* Input frames can be anything as long as they are dataframes with the expected columns.
* This means that CCMNT data will work natively
* The computation for this figure can take a long time if your query period is large!

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
The final output of this sample uses additional ViewClust helper functions to build folders
containing the instantaneous and cumulative job states plotted against their respective targets for each account.
Two additional pages are created. One, plotting the distance from target of an account on the same
axis as other accounts. Two, a helper HTML page which is built to serve as a home page for the summary.

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
            # Call cumu and insta plots wrapped together
            vc.use_suite(clust_target, queued, running, account)

            # Hand information off to lists for later
            account_list.append(account)
            dist_list.append(dist)
            print('Done account: ', account)
        else:
            # Potentially handle differently, but skip for now
            print('Skipped account: ', account)

    # Plot everyone's deviation from target on the same axis:
    vc.delta_plot(account_list,dist_list, 'delta_plot.html')
    # Generate an html page which can link to the various accounts:
    vc.summary_page(account_list, 'all_figures.html')

Things to note about this example:

* The functions use optional arguments. Docstrings are supported in all cases.
* To generate the input job frame, we are using an included slurm helper function
