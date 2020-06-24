import numpy as np
import plotly.graph_objects as go
import sys

def cumu_plot(clust_info, cores_queued, cores_running, resample_str='',
              fig_out='', query_bounds=True, submit_run=[], user_run=[],
              plot_queued=False):
    """Cumulative usage plot.

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
    query_bounds: bool, optional
        Draws red lines on the figure to represent where query is valid.
        Defaults to true.
    submit_run: DataFrame, optional
        Draws a red line representing what would usage have looked like
        if jobs had started instantly. Allows for easier interpretation of
        the queued series. Defaults to not plotting.
    plot_queued: bool, optional
	draw the light blue line indicating the cumulative queued resources.

    See Also
    -------
    jobUse: Generates the input frames for this function.
    """

    print('This function is deprecated as of v0.3.0.\nSupport continues in the ViewClust-Vis package.', file=sys.err)

    # Avoid recalculations via these:
    clust_sum = np.cumsum(clust_info).divide(len(clust_info))
    run_sum = np.cumsum(cores_running).divide(len(clust_info))
    queue_sum = np.cumsum(cores_queued).divide(len(clust_info))

    if resample_str != '':
        clust_sum = clust_sum.resample(resample_str).sum()
        run_sum = run_sum.resample(resample_str).sum()
        queue_sum = queue_sum.resample(resample_str).sum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=clust_info.index,
                             y=clust_sum,
                             fill='tozeroy',
                             mode='none',
                             name='group allocation',
                             fillcolor='rgba(180, 180, 180, .3)'))

    if len(user_run)>0:
        for user in user_run:
            fig.add_trace(go.Scatter(
            x=user_run.index,y=np.cumsum(user_run[user]).divide(len(clust_info)),
            hoverinfo='x+y',
            opacity=.1,
            mode='none',
            name=user,
            stackgroup='use' # define stack group
            ))

    if plot_queued:
	    fig.add_trace(go.Scatter(x=cores_queued.index,
					y=queue_sum,
					mode='lines',
					name='Resources queued',
					marker_color='rgba(160,160,220, .8)'))
    if len(submit_run) > 0:
	    fig.add_trace(go.Scatter(x=submit_run.index,
                             	y=np.cumsum(submit_run).divide(len(clust_info)),
                             	mode='lines',
                             	name='Resources run at submit',
                             	marker_color='rgba(220,160,160, .8)'))
    fig.add_trace(go.Scatter(x=cores_running.index,
                             y=run_sum,
                             mode='lines',
                             name='Resources consumed',
                             marker_color='rgba(80,80,220, .8)'))
    if query_bounds:
        max_y = max(clust_sum.max(), run_sum.max(), queue_sum.max())
        min_x = clust_info.index.min()
        max_x = clust_info.index.max()
        fig.add_shape(dict(type="line", x0=min_x, y0=0, x1=min_x, y1=max_y,
                           line=dict(color="Red", width=2)))
        fig.add_shape(dict(type="line", x0=max_x, y0=0, x1=max_x, y1=max_y,
                           line=dict(color="Red", width=2)))

    fig.update_layout(
        title=go.layout.Title(
            text="Cumulative resource usage: ",
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
                text="Core equivalent in time period",
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
