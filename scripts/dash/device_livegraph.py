import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event

import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
from datetime import datetime


from collections import deque
import plotly.graph_objs as go

app = dash.Dash('Fence-Data')

max_length = 20
times = deque(maxlen=max_length)
## times.append(datetime.now().timestamp())
values = {}
all_items = ['8', '9', '10']
all_names = {'8':'Battery', '9':'Temperature', '10':'Backup-Batt'}

base_url = 'http://leawood:8000/leawood/api/v1'
## log_entry_url=base_url+'/log_entry/'
log_entry_url=base_url+'/last_log/'
device_url=base_url+'/field_device/'
param_url=base_url+'/metadata/'
headers = {'Authorization':'ApiKey admin:40a7590dd47da3443b7fff6dbcdcdfafee5446b8'}

def initUI(device_id):
        ## A list of devices
        ## A list of parameters for a selected device
        item_info_filter = param_url+"?field_device={0}".format(device_id)
        device_params = requests.get(item_info_filter, headers=headers).json()['objects']
        

        

## From the selected devices, grab the lastest data for each and each
## of the selected parameters. In this implementation, I am just concentrating
## on one device. But this should be a dict.
def update_data( times, values, device, items ):
        filter=log_entry_url+"?field_device={0}".format(device)

        try:
                times.append(times[-1]+1)
        except:
                times.append(1)
                
        for item in items:
                if values.get(item) is None:
                        values[item] = deque(maxlen=max_length)
                        
                item_filter = filter+"&param_metadata={0}".format(item)

                item_info_filter = param_url+"?id={0}".format(item)
                item_info = requests.get(item_info_filter, headers=headers).json()['objects'][0]

                response = requests.get(item_filter, headers=headers).json()['objects'][0]
                ## time_stamp = datetime.strptime(response['time_stamp'], '%Y-%m-%dT%H:%M:%S.%f').timestamp()
                item_value = float(response['value'])
                # times.append(time_stamp)
                values[item].append(item_value)
                

        return times, values
        

## Initialise the UI from the database.
## This could be a bit tricky at the moment. The checklist needs
## to actually come from the selected device.


app.layout = html.Div(children=[
        html.Div(children=[
    html.Label('Device'),
    dcc.Dropdown(id='field_device', options =[
            {'label': 'Fence Power 1', 'value':'12'}
            ],
                 value='12'),
    html.Label('Items'),
    ], style={'columnCount':2}),
        html.Div(children=html.Div(id='output-graph'), className='row'),
        dcc.Interval(
                id='graph-update', interval=5*60*1000
                ),
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})


@app.callback(
    Output('output-graph', 'children'),
    [
            Input(component_id='field_device', component_property='value'),
     ],
    events=[Event('graph-update','interval')])
def update_graph(device):
        graph_times, graph_values = update_data(times, values, device, all_items)
        data = []
        graphs = []
        min_times=0
        max_times=0
        min_values=0
        max_values=0
        min_times = min(graph_times)
        max_times = max(graph_times)
        for item in all_items:
                plot = go.Scatter(
                        x=list(graph_times),
                        y=list(graph_values[item]),
                        name='{}'.format(all_names[item]),
                        mode='lines'
                        )
                data.append(plot)
                if min(graph_values[item]) < min_values:
                        min_values = min(graph_values[item])
                if max(graph_values[item]) > max_values:
                        max_values = max(graph_values[item])


        graphs.append(html.Div(dcc.Graph(
                id='device_graph',
                animate=True,
                figure={'data': list(data), 'layout': go.Layout(xaxis=dict(range=[min_times, max_times]),
                                                                yaxis=dict(range=[min_values, max_values]),
                                                                margin={'l':50,'r':10,'t':45,'b':20},
                                                                title='Device - {}'.format(device))}
                ), className=''))
        return graphs



external_css = ["https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js',
               'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})



if __name__ == '__main__':
        update_data(times, values, '12', all_items)
        app.run_server(debug=True)


