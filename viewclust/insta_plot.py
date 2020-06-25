import plotly.graph_objects as go
import sys

def insta_plot(clust_info, cores_queued, cores_running, resample_str='',
               fig_out='', y_label='Usage', fig_title='', query_bounds=True, submit_run=[], user_run=[]):
    """Instantaneous usage plot.

    This function is deprecated as of v0.3.0.
    
    Support continues in the ViewClust-Vis package.


    Parameters
    -------
    clust_info: DataFrame
        Frame which represents the cluster state at given time intervals. See jobUse.
    cores_queued: array_like of DataFrame
        Series displaying queued resources at a particular time. See jobUse.
    cores_running: array_like of DataFrame
        Series displaying running resources at a particular time. See jobUse.
    resample_str: pandas freq str, optional
        Defaults to empty, meaning no resampling. Passing this parameter
        does not do sanity checking and will only run the below code example.
        cores_queued = cores_queued.resample('1D').sum()
    fig_out: str, optional
        Writes the generated figure to file as the given name.
        If empty, skips writing. Defaults to empty.
    y_label: str, optional
        Makes the passed string the y-axis label.
    fig_title: str, optional
        Appends the given string to the title.
    query_bounds: bool, optional
        Draws red lines on the figure to represent where query is valid.
        Defaults to true.
    submit_run: DataFrame, optional
        Draws a red line representing what would usage have looked like
        if jobs had started instantly. Allows for easier interpretation of
        the queued series. Defaults to not plotting.

    See Also
    -------
    jobUse: Generates the input frames for this function.
    """

    print('This function is deprecated as of v0.3.0.\nSupport continues in the ViewClust-Vis package.', file=sys.err)

    # Temp vars so that we aren't touching anything by ref
    clust_info_tmp = clust_info.copy()
    cores_queued_tmp = cores_queued.copy()
    cores_running_tmp = cores_running.copy()

    if resample_str != '':
        clust_info_tmp = clust_info_tmp.resample(resample_str).sum()
        cores_queued_tmp = cores_queued_tmp.resample(resample_str).sum()
        cores_running_tmp = cores_running_tmp.resample(resample_str).sum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=clust_info_tmp.index, y=clust_info_tmp,
                             fill='tozeroy',
                             mode='none',
                             name='Allocation',
                             fillcolor='rgba(180, 180, 180, .3)'))

    if len(user_run)>0:
        for user in user_run:
            fig.add_trace(go.Scatter(
            x=user_run.index,y=user_run[user],
            line=dict(width=0),
            hoverinfo='x+y',
            opacity=.1,
            mode='none',
            name=user,
            stackgroup='use' # define stack group
            ))


    fig.add_trace(go.Scatter(x=cores_queued_tmp.index, y=cores_queued_tmp,
                             mode='lines',
                             name='Resources queued',
                             marker_color='rgba(160,160,220, .8)'))
    if len(submit_run) > 0:
        submit_run_tmp = submit_run.copy()
        if resample_str != '':
            submit_run_tmp = submit_run_tmp.resample(resample_str).sum()

        fig.add_trace(go.Scatter(x=submit_run_tmp.index, y=submit_run_tmp,
                             	mode='lines',
                             	name='Resources run at submit',
                             	marker_color='rgba(220,80,80, .8)'))
    fig.add_trace(go.Scatter(x=cores_running_tmp.index, y=cores_running_tmp,
                             mode='lines',
                             name='Resources running',
                             marker_color='rgba(80,80,220, .8)'))

    if query_bounds:
        max_y = max(cores_running.max(), cores_queued.max())
        min_x = clust_info.index.min()
        max_x = clust_info.index.max()
        fig.add_shape(dict(type="line", x0=min_x, y0=0, x1=min_x, y1=max_y,
                           line=dict(color="Red", width=2)))
        fig.add_shape(dict(type="line", x0=max_x, y0=0, x1=max_x, y1=max_y,
                           line=dict(color="Red", width=2)))

    fig.update_layout(
        title=go.layout.Title(
            text="Resource usage: " + fig_title,
            xref="paper",
            x=0
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text="Date Time",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text=y_label,
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
        )
    )
    if fig_out != '':
        fig.write_html(fig_out)

    return fig
