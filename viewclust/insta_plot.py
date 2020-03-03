import plotly.graph_objects as go

def insta_plot(clust_info, cores_queued, cores_running,
               fig_out='', y_label='Usage', fig_title='', query_bounds=True):
    """Instantaneous usage plot.

    Parameters
    -------
    clust_info: DataFrame
        Frame which represents the cluster state at given time intervals. See jobUse.
    cores_queued: array_like of DataFrame
        Series displaying queued resources at a particular time. See jobUse.
    cores_running: array_like of DataFrame
        Series displaying running resources at a particular time. See jobUse.
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

    See Also
    -------
    jobUse: Generates the input frames for this function.
    """

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=clust_info.index, y=clust_info,
                             fill='tozeroy',
                             mode='none',
                             name='Allocation',
                             fillcolor='rgba(180, 180, 180, .3)'))
    fig.add_trace(go.Scatter(x=cores_queued.index, y=cores_queued,
                             mode='lines',
                             name='Resources queued',
                             marker_color='rgba(160,160,220, .8)'))
    fig.add_trace(go.Scatter(x=cores_running.index, y=cores_running,
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
