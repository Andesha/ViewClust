import pandas as pd

def node_use(node_states, debugging=False):
    """Calculate node usage statistics based on polling database.

    Consider resampling data to get into hour format for easier plotting.

    Returns
    -------
    cores_total:
        Series, total numbers of cores the scheduler is seeing at any point.
    cores_perc:
        Series, weighted average (cpus in node) of alloc cpu over cfg cpu.
        Read as percentage of cpus in use.
    mem_perc:
        Series, weighted average (cpus in node) of alloc mem over cfg mem.
        Read as percentage of memory in use.
    max_perc:
        Series, weighted average (cpus in node)
    """

    if debugging:
        print('Calculating percentage measures...')
    node_states['p_cpu'] = node_states['a_cpu']/node_states['t_cpu']
    node_states['p_mem'] = node_states['a_mem']/node_states['t_mem']
    node_states['p_max'] = node_states[['p_cpu', 'p_mem']].max(axis=1)

    if debugging:
        print('Calculating sum measures...')
    cores_total = node_states.groupby(pd.Grouper(freq='H')).sum()['t_cpu']

    # Quick weighted average
    def w_avg(group, avg_name, weight_name):
        data = group[avg_name]
        weights = group[weight_name]
        return (data * weights).sum() / weights.sum()

    cores_perc = node_states.groupby(pd.Grouper(freq='H')).apply(w_avg, "p_cpu", "t_cpu")
    mem_perc = node_states.groupby(pd.Grouper(freq='H')).apply(w_avg, "p_mem", "t_cpu")
    max_perc = node_states.groupby(pd.Grouper(freq='H')).apply(w_avg, "p_max", "t_cpu")

    return cores_total, cores_perc, mem_perc, max_perc
