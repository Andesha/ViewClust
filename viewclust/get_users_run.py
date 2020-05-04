from viewclust.job_use import job_use
import pandas as pd

def get_users_run(jobs, d_from, target, d_to='', use_unit='cpu'):
    """Takes a DataFrame full of job information and returns usage for each "user" 
    uniquely based on specified unit.

    This function operates as a stepping stone for plotting usage figures
    and returns various series and frames for several different uses.

    Parameters
    -------
    jobs: DataFrame
        Job DataFrame typically generated by slurm/sacct_jobs or the ccmnt package.
    use_unit: str, optional
        Usage unit to examine. One of: {'cpu', 'cpu-eqv', 'gpu', 'gpu-eqv'}.
        Defaults to 'cpu'.
    d_from: date str
        Beginning of the query period, e.g. '2019-04-01T00:00:00'.
    target: int-like
        Typically a cpu allocation or core eqv value for a particular acount, often 50.
    d_to: date str, optional
        End of the query period, e.g. '2020-01-01T00:00:00'. Defaults to now if empty.

    Returns
    -------
    user_running_cat:
        Frame of running resources for each of the unique "users" in the jobs data frame
    """

    users = jobs.user.unique()
    
    user_count=0
    for user in users:
        user_mask=jobs['user'].str.match(user)
        user_jobs=jobs[user_mask].copy()
        _,user_queued,user_running,_ = job_use(user_jobs, d_from, target, d_to=d_to, use_unit='cpu')

        user_queued=user_queued[d_from:d_to]
        user_running=user_running[d_from:d_to]

        if user_count == 0:
            user_running_cat = pd.Series(user_running,index=user_running.index,name=user)
        else:
            user_running_ser = pd.Series(user_running,index=user_running.index,name=user)
            user_running_cat = pd.concat([user_running_cat, user_running_ser], axis=1)

        user_count = user_count + 1

    return user_running_cat