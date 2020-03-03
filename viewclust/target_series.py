import pandas as pd

def target_series(time_frames):
    """Takes a list of tuples and builds a target based time series.

    Parameters
    -------
    time_frames: list, tuples of 3
        List should be something of the following form:
            # Q4:
            d_from = '2019-10-01T00:00:00'
            d_dec = '2019-12-01T00:00:00'
            d_to = '2019-12-31T00:00:00'

            time_frames = [(d_from,d_dec,100),(d_dec,d_to,500)]

    Returns
    -------
    tar_frame: Pandas Series
        Time series by hour of the time_frames list.
        Based on above example:
            2019-10-01 00:00:00      100
            2019-10-01 01:00:00      100
            2019-10-01 02:00:00      100
            2019-10-01 03:00:00      100
            2019-10-01 04:00:00      100
            ...                      ...
            2019-12-30 20:00:00      500
            2019-12-30 21:00:00      500
            2019-12-30 22:00:00      500
            2019-12-30 23:00:00      500
            2019-12-31 00:00:00      500

    See Also
    -------
    jobUse: Generates the input frame for this function.
    """

    series_list = []
    for period in time_frames:
        query_period = pd.date_range(start=period[0], end=period[1], freq='H')
        new_series = pd.Series(index=query_period)
        new_series = new_series.fillna(pd.to_numeric(period[2]))
        series_list.append(new_series)

    tar_frame = pd.Series()
    for period in series_list:
        tar_frame = tar_frame.append(period)

    # Avoid overlapping by keeping first
    tar_frame = tar_frame.groupby(tar_frame.index).first()

    return tar_frame
