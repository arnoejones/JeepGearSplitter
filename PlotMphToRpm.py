# Purpose: User interface to display and compare RPM and MPH values in a plot.
#
# Author:      Arno E Jones
#
# Created:     10/08/2018
# Copyright:   (c) jonesar 2018
# Licence:     This code can be freely shared and modified as long as the author is credited with the original (this) version.
#-------------------------------------------------------------------------------

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

import Calculate
import WranglerRatiosLookup
import GetTransmissionRatios

app = dash.Dash()

# default chart that appears
final_dict = {'jeep_model': 'jk_2012',
              'transmissionType': 'auto',
              'rubicon': True,
              'fourLowEngaged': False,
              'tireDiameter': 33.4,
              'diffGearRatio': 4.56,
              'gearSelected': 5}

diff_list = []
for diff in WranglerRatiosLookup.wrangler_diff_ratios():
    diff_list.append({'label': str(diff) + ':1', 'value': diff})

jeep_model_list = []
for key, value in WranglerRatiosLookup.jeep_model_dict().items():
    jeep_model_list.append({'label': key, 'value': value})

app.layout = \
    html.Div([
        html.Div('Welcome to Jeep Gear Splitter',
                 id='title-div',
                 className='title-div-class'
                 ),
        html.Div([
            html.H4('Choose a Jeep'),
            dcc.Dropdown(
                id="jeep-dropdown-id",
                options=jeep_model_list,
                value='jk_2012', ),
            html.Div(id='jeep-model-div'),

            html.H4("Transmission"),
            dcc.RadioItems(
                id='tranny_id',
                options=[{'label': 'Automatic', 'value': 'auto'},
                         {'label': ' Manual', 'value': 'manual'}],
                value='auto'),
            html.Div(id='tranny-div'),

            html.H4("Rubicon?"),
            dcc.RadioItems(
                id='rubi-id',
                options=[{'label': 'Yes', 'value': True},
                         {'label': 'No', 'value': False}],
                value=True),
            html.Div(id='rubi-div'),

            html.H4("Transfer Case:"),
            dcc.RadioItems(
                id='tcase_id',
                options=[{'label': ' Engaged ', 'value': True},
                         {'label': 'Not Engaged', 'value': False}],
                value=False),
            html.Div(id='tcase-div'),

            html.H4("Diff Gear Ratio"),
            dcc.Dropdown(id="diff-ratio-id",
                         options=diff_list,
                         value=4.56, ),
            html.Div(id='diff-ratio-div'),

            html.H4("Tire Diameter (inches):"),
            html.H6("Measure from center to the ground x 2"),
            dcc.Input(
                id='tire_id',
                value=33.4,
                type='float'),
            html.Div(id='tire-div'),
        ], className='buttons-div-class'),

        html.Div([
            html.Div(
                dcc.Graph(id='graph', className='graph-div-class')
            )
        ]),

        html.Div([html.Button('Click to Recalculate Graph', id='button')],
                 id='button-div',
                 className='button-div-class'),

    ], className='grid-container')

# ... plot callbacks ...

@app.callback(Output(component_id='diff-ratio-div', component_property='children'),
              [Input(component_id='diff-ratio-id', component_property='value')])
def diff_ratio_callback(diff_ratio_input_value):
    final_dict['diffGearRatio'] = diff_ratio_input_value


@app.callback(Output(component_id='jeep-model-div', component_property='children'),
              [Input(component_id='jeep-dropdown-id', component_property='value')])
def jeep_model_callback(jeep_model_input_value):
    final_dict['jeep_model'] = jeep_model_input_value


@app.callback(Output(component_id='tranny-div', component_property='children'),
              [Input(component_id='tranny_id', component_property='value')])
def tranny_callback(tranny_input_value):
    final_dict['transmissionType'] = tranny_input_value


@app.callback(Output(component_id='rubi-div', component_property='children'),
              [Input(component_id='rubi-id', component_property='value')])
def rubicon_callback(rubicon_input_value):
    final_dict['rubicon'] = rubicon_input_value


@app.callback(Output(component_id='tcase-div', component_property='children'),
              [Input(component_id='tcase_id', component_property='value')])
def tcase_callback(tcase_input_value):
    final_dict['fourLowEngaged'] = tcase_input_value


@app.callback(Output(component_id='tire-div', component_property='children'),
              [Input(component_id='tire_id', component_property='value')])
def tire_callback(tire_input_value):
    final_dict['tireDiameter'] = float(tire_input_value)


@app.callback(Output('graph', 'figure'),
              [Input('button', 'n_clicks')])
def update_figure(n_clicks):
    gear_ratios = GetTransmissionRatios.GetTransmissionRatios.get_trans_ratios(final_dict)

    transfercase_final_value = GetTransmissionRatios.GetTransmissionRatios.get_tcase_ratios(final_dict)

    traces = []

    for gear_index in range(0, len(gear_ratios)):
        df = pd.DataFrame(Calculate.JeepGearSplitter.calculateSpeedFromRpm(
            differentialGearRatio=final_dict['diffGearRatio'],
            tireDiameter=final_dict['tireDiameter'],
            transmissionGearRatio=gear_ratios[gear_index],
            transferCaseRatio=transfercase_final_value
        )).transpose()
        df.columns = ['RPM', 'MPH']

        if gear_index == 0:
            gear_index = "Reverse"
        if gear_index == 1:
            gear_index = "1st"
        if gear_index == 2:
            gear_index = "2nd"
        if gear_index == 3:
            gear_index = "3rd"
        if gear_index == 4:
            gear_index = "4th"
        if gear_index == 5:
            gear_index = "5th"
        if gear_index == 6:
            gear_index = "6th"
        if gear_index == 7:
            gear_index = "7th"
        if gear_index == 8:
            gear_index = "8th"

        trace = go.Scatter(x=df['RPM'],
                           y=df['MPH'],
                           name=gear_index
                           )
        traces.append(trace)

    layout = go.Layout(title='Transmission Gear Ratio Comparisons',
                       xaxis={'title': 'RPM'},
                       yaxis={'title': 'MPH'})

    return {'data': traces, 'layout': layout}


if __name__ == '__main__':
    app.run_server()
