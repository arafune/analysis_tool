#!/usr/bin/env python3
"""Web dashboard for the multimonitor.

Use dash with plotly.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
import logging
import output


logging.getLogger('werkzeug').setLevel(logging.ERROR)
dummy = False
try:
    import sensor_set_a
except ImportError:
    dummy = True

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
data = {
    'date_time': [],
    'T1': [],
    'T2': [],
    'T3': [],
    'T4': [],
    'Pres_A': [],
    'Pres_P': [],
    'v3': [],
    'v4': [],
    'v5': []
}

logfile = open('log.txt', mode='a+')
logfile.write('#date\tT1\tT2\tT3\tT4\tPressure(A)\tPressure(P)\t')
logfile.write('v3\tv4\tv5\n')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.H1(children='Multi monitor system Dashboard'),
    html.Div(id='live-update-text'),
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(id='interval-component', interval=3 * 1000, n_intervals=0)
])


@app.callback(
    Output('live-update-graph', 'figure'),
    [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    """Live update graph by using dash with plotly."""
    fig = plotly.tools.make_subplots(
        rows=2, cols=2, vertical_spacing=0.01, shared_xaxes=True, print_grid=False)
    fig['layout']['margin'] = {'l': 50, 'r': 30, 'b': 40, 't': 0}
    fig['layout']['legend'] = {
        'x': 1.,
        'y': .88,
        'xanchor': 'left',
        'yanchor': 'top'
    }
    fig['layout'].update(height=650)
    fig['layout']['yaxis2'].update(
        title='Pressure (mbar)', type='log', exponentformat='power')
    fig['layout']['yaxis'].update(title='Temperature (C)')
    fig['layout']['yaxis3'].update(title='Voltage  (V)')

    # temperature
    fig.append_trace({
        'x': data['date_time'],
        'y': data['T1'],
        'name': 'Temperature1',
        'mode': 'lines',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': data['date_time'],
        'y': data['T2'],
        'name': 'Temperature2',
        'mode': 'lines',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': data['date_time'],
        'y': data['T3'],
        'name': 'Temperature3',
        'mode': 'lines',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': data['date_time'],
        'y': data['T4'],
        'name': 'Temperature4',
        'mode': 'lines',
        'type': 'scatter'
    }, 1, 1)

    #
    fig.append_trace({
        'x': data['date_time'],
        'y': data['Pres_A'],
        'name': 'Pressure (A)',
        'mode': 'lines',
        'type': 'scatter'
    }, 1, 2)
    fig.append_trace({
        'x': data['date_time'],
        'y': data['Pres_P'],
        'name': 'Pressure (P)',
        'mode': 'lines',
        'type': 'scatter'
    }, 1, 2)

    #
    fig.append_trace({
        'x': data['date_time'],
        'y': data['v3'],
        'name': 'V3',
        'mode': 'lines',
        'type': 'scatter'
    }, 2, 1)
    fig.append_trace({
        'x': data['date_time'],
        'y': data['v4'],
        'name': 'v4',
        'mode': 'lines',
        'type': 'scatter'
    }, 2, 1)
    fig.append_trace({
        'x': data['date_time'],
        'y': data['v5'],
        'name': 'V5',
        'mode': 'lines',
        'type': 'scatter'
    }, 2, 1)

    return fig


@app.callback(
    Output('live-update-text', 'children'),
    [Input('interval-component', 'n_intervals')])
def update_values(n):
    """Read values from the sensors, store them and display them."""
    if dummy:
        now, t1, t2, t3, t4, ana, prep, v3, v4, v5 = output.dummy(9)
    else:
        now, t1, t2, t3, t4, ana, prep, v3, v4, v5 = sensor_set_a.read()
    output.publish((now, t1, t2, t3, t4, ana, prep, v3, v4, v5),
                   logfile=logfile)
    style = {'padding': '5px', 'fontSize': '24px'}
    data['date_time'].append(now)
    data['T1'].append(t1)
    data['T2'].append(t2)
    data['T3'].append(t3)
    data['T4'].append(t4)
    data['Pres_A'].append(ana)
    data['Pres_P'].append(prep)
    data['v3'].append(v3)
    data['v4'].append(v4)
    data['v5'].append(v5)
    if len(data['date_time']) > 150:
        del data['date_time'][0]
        del data['T1'][0]
        del data['T2'][0]
        del data['T3'][0]
        del data['T4'][0]
        del data['Pres_A'][0]
        del data['Pres_P'][0]
        del data['v3'][0]
        del data['v4'][0]
        del data['v5'][0]
    return [
        html.Span("{}  ".format(now.strftime('%Y-%m-%d %H:%M:%S')), style=style),
        # html.Br(),
        html.Span('Temp 1: {0:6.2f} C, '.format(t1), style=style),
        html.Span('Temp 2: {0:6.2f} C, '.format(t2), style=style),
        html.Span('Temp 3: {0:6.2f} C, '.format(t3), style=style),
        html.Span('Temp 4: {0:6.2f} C, '.format(t4), style=style),
        html.Br(),
        html.Span('Pressure (A): {0:.3E} mbar,'.format(ana), style=style),
        html.Span('Pressure (P): {0:.3E} mbar  '.format(prep), style=style),
        # html.Br(),
        html.Span('V3: {0:6.3f} V, '.format(v3), style=style),
        html.Span('V4: {0:6.3f} V, '.format(v4), style=style),
        html.Span('V5: {0:6.3f} V, '.format(v5), style=style),
    ]


if __name__ == '__main__':
    app.run_server(debug=False, host='192.168.1.2')
