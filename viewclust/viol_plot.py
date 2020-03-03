from datetime import datetime
import plotly.graph_objects as go

def viol_plot(d_from, cores_queued, cores_running, target, d_to='', fig_out=''):
    """Violin distribution usage plot.

    Parameters
    -------
    d_from: date str
        Beginning of the query period, e.g. '2019-04-01T00:00:00'
    cores_queued: array_like of DataFrame
        Series displaying queued resources at a particular time. See jobUse.
    cores_running: array_like of DataFrame
        Series displaying running resources at a particular time. See jobUse.
    target: int
        Target information for a given usage. Can be user specific or system-wide.
    d_to: date str, optional
        End of the query period, e.g. '2020-01-01T00:00:00'. If empty, defaults to now.
    fig_out: str, optional
        Writes the generated figure to file as the given name.
        If empty, skips writing. Defaults to empty.

    See Also
    -------
    jobUse: Generates the input frames for this function.
    """

    # d_to boilerplate
    if d_to == '':
        now = datetime.now()
        d_to = now.strftime('%Y-%m-%dT%H:%M:%S')

    fig = go.Figure()
    fig.add_trace(go.Violin(y=cores_running.loc[d_from:d_to].divide(int(target)) * 100,
                            points='all', # show all points
                            jitter=0.05,  # add some jitter on points for better visibility
                            side='positive',
                            pointpos=-.1,
                            line_color='rgba(80,80,220, .8)',
                            name='Total CPUs running'))
    fig.add_trace(go.Violin(y=cores_queued.loc[d_from:d_to].divide(int(target)) * 100,
                            points='all', # show all points
                            jitter=0.05,  # add some jitter on points for better visibility
                            side='negative',
                            pointpos=.1,
                            line_color='rgba(220,80,80, .8)',
                            name='RAC CPUs running'))

    # update characteristics shared by all traces
    fig.update_traces(meanline_visible=True,
                      box_visible=True,
                      opacity=0.6,
                      scalemode='count') #scale violin plot area with total count

    fig.update_layout(
        title_text="CPU utilization: ",
        violingap=0, 
        violingroupgap=0, 
        violinmode='overlay',
        yaxis_title='Percent CPU capacity',
        xaxis_title='Time bin count',
        showlegend=False)

    if fig_out != '':
        fig.write_html(fig_out)
