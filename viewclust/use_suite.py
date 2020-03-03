from pathlib import Path
import viewclust as vc

def use_suite(clust_info, cores_queued, cores_running, folder):
    """Creates a folder of a given name and creates figures inside of it.

    Function is intended to be called in a loop over a list of accounts.
    Folder parameter should most often be the current account name.

    Parameters
    -------
    clust_info: DataFrame
        Frame which represents the cluster state at given time intervals. See jobUse.
    cores_queued: array_like of DataFrame
        Series displaying queued resources at a particular time. See jobUse.
    cores_running: array_like of DataFrame
        Series displaying running resources at a particular time. See jobUse.
    Folder: str
        Folder to place generated figures inside of.
        Typically an account name.

    See Also
    -------
    jobUse: Generates the input frames for this function.
    summaryPage: Can build an html page based on all figures generated
    """

    # Handle folder creation
    safe_folder = folder
    if safe_folder[-1] != '/':
        safe_folder += '/'
    Path(safe_folder).mkdir(parents=True, exist_ok=True)

    # Add more to the suite as you like
    vc.cumu_plot(clust_info, cores_queued, cores_running, safe_folder+'cumu_plot.html')
    vc.insta_plot(clust_info, cores_queued, cores_running, safe_folder+'insta_plot.html')
