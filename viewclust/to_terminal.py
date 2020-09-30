from typing import Union, Optional, List
import pandas as pd
import plotille
import os


def to_terminal(series: Union[pd.Series, List[pd.Series]],
                title: str = 'resource usage',
                pu: str = 'cpu', labels: Optional[list] = None):
    """
    Plot a datetime series (or a list of them) to terminal

    Parameters
    -------
    series:
        A datetime series or a list of series to be plot
    title:
        Title for the plot
    pu:
        Processing using (GPU or CPU) for y axis
    labels:
        If multiple series, the labels of each ome
    """

    size = os.get_terminal_size()
    colors = ['blue', 'yellow', 'magenta', 'cyan', 'white', 'green']
    if not isinstance(series, list):
        series = [series]
    if labels is None:
        labels = [None for _ in range(len(series))]
    else:
        if len(labels) != len(series):
            raise Exception('Labels do not match inputs')
    print(title.center(size.columns))
    fig = plotille.Figure()
    fig.color_mode = 'names'
    fig.x_label = 'Dates'
    fig.y_label = f'{pu} count'
    for idx, s in enumerate(series):
        s = s.map('{:.2f}'.format).astype(float)
        x = s.index
        y = s.values
        q1 = s.quantile(0.1)
        fig.set_x_limits(min_=min(x), max_=max(x))
        fig.set_y_limits(min_=min(y) - q1, max_=max(y) + q1)
        fig.plot(x, y, lc=colors[idx], label=labels[idx])
    print(fig.show(legend=True))
