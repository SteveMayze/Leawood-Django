import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import requests
import json
import pandas as pd
from pandas.io.json import json_normalize

app = dash.Dash()

base_url = 'http://leawood:8000/leawood/api/v1'
log_entry_url=base_url+'/log_entry/'
device_url=base_url+'/field_device/'
param_url=base_url+'/metadata/'
headers = {'Authorization':'ApiKey admin:40a7590dd47da3443b7fff6dbcdcdfafee5446b8'}



app.layout = html.Div(children=[
        html.Div(children=[
    html.Label('Device'),
    dcc.Dropdown(id='field_device', options =[
            {'label': 'Fence Power 1', 'value':'12'}
            ],
                 value='12'),
    html.Label('Items'),
    dcc.Checklist(id='item', options=[
            {'label':'backup battery', 'value':'10'},
            {'label':'battery', 'value':'8'},
            {'label':'temperature', 'value':'9'},            
            ],
                  values=['8'])
    ], style={'columnCount':2}),
    html.Div(id='output-graph'),
])



@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [
            Input(component_id='field_device', component_property='value'),
            Input(component_id='item', component_property='values')
     ]
)
def update_value(device, items):
        print("value={0} item={1}".format(device, items))
        filter=log_entry_url+"?field_device={0}".format(device)

        data = []
        for item in items:
                print("item={0}".format(item))
                item_filter = filter+"&param_metadata={0}".format(item)

                item_info_filter = param_url+"?id={0}".format(item)
                item_info = requests.get(item_info_filter, headers=headers).json()['objects'][0]

                response = requests.get(item_filter, headers=headers).json()['objects']
                df = json_normalize(response)
                print("name={0}".format(item_info['name']))
                data.append({'x':df.index, 'y':df.value, 'type':'line', 'name':item_info['name']})

        print('DF={}'.format(df) )
        print('DATA={}'.format(data) )

        return dcc.Graph(id='device_graph',
                         figure={
                                 'data': data,
                                 'layout': {
                                         'title':'Device Graph'
                                         }
                                 })

if __name__ == '__main__':
	app.run_server(debug=True)


