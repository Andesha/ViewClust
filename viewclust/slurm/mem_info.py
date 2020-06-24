import subprocess
import pandas as pd

import plotly.graph_objects as go

def mem_info(d_from, account, fig_out='', debugging=False):
    """Script for profiling the memory usage of an account via sacct.

    Always outputs various statistical measures to stdout, but can
    also plot information.

    Parameters
    -------
    d_from: date str
        Beginning of the query period, e.g. '2019-04-01T00:00:00'.
    account: str
        Account to query via sacct, e.g. 'def-tk11br_cpu'
    fig_out: str, optional
        Writes the generated figure to file as the given name.
        If empty, skips writing. Defaults to empty.
    debugging: boolean, optional
        Boolean for reporting progress to stdout. Default False.
    """

    base_cmd = ['sacct', '-a', '-A', account, '-S', d_from,
                '-p', '--delimiter', '"|"', '-n',
                '--units=M', '-o', 'jobid,submit,start,state,ncpus,nnodes,reqmem,maxrss']
    data = subprocess.check_output(base_cmd).decode('UTF-8')

    if debugging:
        print('Query complete')

    mem_frame = pd.DataFrame([x.split('"|"') for x in data.split('\n')])
    # Below two drops are tested for both loading from file and raw string loading
    mem_frame = mem_frame.iloc[:, :-1] # Due to split implementation...
    mem_frame = mem_frame.iloc[:-1, :] # Due to split implementation...

    if debugging:
        print('Frame built')

    # Edge case before things start to happen...
    if mem_frame.empty:
        print('No job records found.')
        return

    mem_frame.columns = ['name','submit','start','state','reqcpus','nnodes','reqmem','maxrss']

    mem_frame = mem_frame[mem_frame.name.str.contains('batch', na=False)]
    mem_frame = mem_frame[mem_frame.maxrss.str.contains('M', na=False)]
    mem_frame.update(mem_frame.maxrss.loc[lambda x: x.str.contains('M')] \
                    .str.replace('M', ''))
    mem_frame['maxrss'] = pd.to_numeric(mem_frame['maxrss'])

    mem_frame['nnodes'] = pd.to_numeric(mem_frame['nnodes'])
    mem_frame['reqcpus'] = pd.to_numeric(mem_frame['reqcpus'])

    # Construct alloc_mem column
    mem_frame['memHold'] = mem_frame['reqmem'].map(lambda x: int(x.lstrip('+-').rstrip('MmNnCc')))
    core_mask = (mem_frame['reqmem'].str.contains('c'))
    node_mask = (mem_frame['reqmem'].str.contains('n'))
    print(mem_frame)
    mem_frame.loc[core_mask, 'memHold'] = (mem_frame['reqcpus'] * mem_frame['memHold'])
    mem_frame.loc[node_mask, 'memHold'] = (mem_frame['nnodes'] * mem_frame['memHold'])
    mem_frame = mem_frame.rename(columns={'memHold':'alloc_mem'})
    
    mem_frame['submit'] = pd.to_datetime(mem_frame['submit'])

    if debugging:
        print('Done column building')

    print('Units is MB:')
    print(mem_frame['maxrss'].describe())

    if fig_out != '':
        x_points = []
        y_points = []
        for _, row in mem_frame.iterrows():
		        c_x_points = [row['submit'], row['start'], None]
		        x_points = x_points + c_x_points
	
		        c_y_points = [row['alloc_mem']/1000,row['maxrss']/1000, None]
		        y_points = y_points + c_y_points
                
        fig = go.Figure(data=go.Scatter(
		        x=x_points,
		        y=y_points,
		        mode='lines',
		        line_color='rgba(180,180,180, .1)',
		        name='target'))
                
        fig.add_trace(go.Scatter(
		        x=mem_frame['submit'],
		        y=mem_frame['alloc_mem']/1000,
		        mode='markers',
		        line_color='rgba(220,60,60, .4)',
		        name='alloc mem',
		        hovertext=mem_frame['name']))
                
        fig.add_trace(go.Scatter(
		        x=mem_frame['start'],
		        y=mem_frame['maxrss']/1000,
		        mode='markers',
		        line_color='rgba(60,180,60, .4)',
		        name='maxrss',
		        hovertext=mem_frame['name']))
                
        fig.write_html(fig_out)


