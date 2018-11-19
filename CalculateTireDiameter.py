# Purpose: User interface to display effective tire diameter.
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
from dash.dependencies import Input, Output, State
import WranglerRatiosLookup
import Calculate
import GetTransmissionRatios

app = dash.Dash()

jeep_model_list = []
for key, value in WranglerRatiosLookup.jeep_model_dict().items():
    jeep_model_list.append({'label': key, 'value': value})
    print(key, value)

diff_list = []
for diff in WranglerRatiosLookup.wrangler_diff_ratios():
    diff_list.append({'label': str(diff) + ':1', 'value': diff})

app.layout = html.Div([
    html.H3("To display your actual, effective tire diameter, take a snapshot of your RPM and MPH in top gear, say, from "
            "Torque or DB Fusion and enter those values.  The result is the effective tire diameter.  The effective "
            "diameter is what your running gear sees, not the diameter of the tire as measured from one end of the tire "
            "to the other, or even from the floor to the top of the tire.  Not only is there a rather large margin of "
            "error in trying to take that measurement, it's also the wrong place to measure.  The only accurate "
            "static measurement for the effective diameter is to measure from the floor to the center and double that."),
    html.Div([
        dcc.Input(id='mph-in',
                  value=70,  # default display value
                  debounce=True,  # don't update until string is complete
                  type='float'  # return a float, not a string
                  ), ' Enter MPH',  # display string
        html.Div(id='mph-out')  # id for this Div
    ], className='mph-div'),  # class name for this div for the splitter.css link

    html.Div([
        dcc.Input(id='rpm-in',
                  value=2666,
                  debounce=True,
                  type='float'
                  ), ' Enter RPM',
        html.Div(id='rpm-out')
    ], className='rpm-div'),
    html.Div([
        dcc.Dropdown(
            id="jeep-dropdown-id",
            options=jeep_model_list,
            value='jk_2012'), 'Jeep Model',
        html.Div(id='jeep-model-div')
    ], className='jeep-div'),

    html.Div([
        dcc.RadioItems(
            id='tranny_id',
            options=[{'label': 'Automatic', 'value': 'auto'},
                     {'label': ' Manual', 'value': 'manual'}],
            value='auto'), 'Transmission Type',
        html.Div(id='tranny-div')
    ], className='tranny-div'),

    html.Div([
        dcc.RadioItems(
            id='rubi-id',
            options=[{'label': 'Yes', 'value': True},
                     {'label': 'No', 'value': False}],
            value=True), 'Rubicon Transfer Case?',
        html.Div(id='rubi-div')
    ], className='rubi-div'),

    html.Div([
        dcc.RadioItems(
            id='tcase_id',
            options=[{'label': ' Engaged ', 'value': True},
                     {'label': 'Not Engaged', 'value': False}],
            value=False), 'Transfer Case Engaged?',
        html.Div(id='tcase-div')
    ], className='tcase-div'),

    html.Div([
        dcc.Dropdown(id="diff-ratio-id",
                     options=diff_list,
                     value=4.88), 'Differential Ratio',
        html.Div(id='diff-ratio-div')
    ], className='diff-div'),

    html.Div([
        html.Button(id='submit-button',
                    n_clicks=0,
                    children='Calculate Tire Diameter',
                    style={'fontSize': 24}),
        html.H1(id='number-out')
    ], className='button-div')
], className='master-div')

numbers_dict = {'mph': 70,
                'rpm': 2666,
                'jeep_model': 'jk_2012',
                'transmissionType': 'auto',
                'rubicon': True,
                'fourLowEngaged': False,
                'differentialGearRatio': 4.56,
                'gearSelected': 5}


@app.callback(Output('diff-ratio-div', 'children'),
              [Input('diff-ratio-id', 'value')])
def commit_diff_ratio(diff_ratio):
    numbers_dict['differentialGearRatio'] = float(diff_ratio)


@app.callback(Output('mph-out', 'children'),
              [Input('mph-in', 'value')])
def commit_mph(mph_value):
    numbers_dict['mph'] = float(mph_value)


@app.callback(Output('rpm-out', 'children'),
              [Input('rpm-in', 'value')])
def commit_rpm(rpm_value):
    numbers_dict['rpm'] = float(rpm_value)


@app.callback(Output(component_id='jeep-model-div', component_property='children'),
              [Input(component_id='jeep-dropdown-id', component_property='value')])
def jeep_model_callback(jeep_model_input_value):
    numbers_dict['jeep_model'] = jeep_model_input_value


@app.callback(Output(component_id='tranny-div', component_property='children'),
              [Input(component_id='tranny_id', component_property='value')])
def tranny_callback(tranny_input_value):
    numbers_dict['transmissionType'] = tranny_input_value


@app.callback(Output(component_id='rubi-div', component_property='children'),
              [Input(component_id='rubi-id', component_property='value')])
def rubicon_callback(rubicon_input_value):
    numbers_dict['rubicon'] = rubicon_input_value


@app.callback(Output(component_id='tcase-div', component_property='children'),
              [Input(component_id='tcase_id', component_property='value')])
def tcase_callback(tcase_input_value):
    numbers_dict['fourLowEngaged'] = tcase_input_value


@app.callback(Output('number-out', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('mph-in', 'value')])
def display_tire_size(some_number, some_value):
    gear_ratios = GetTransmissionRatios.GetTransmissionRatios.get_trans_ratios(numbers_dict)

    transfercase_final_value = GetTransmissionRatios.GetTransmissionRatios.get_tcase_ratios(numbers_dict)

    tire_diameter = float("{0:.2f}".format(Calculate.JeepGearSplitter.calculateTireDiameter(mph=numbers_dict['mph'],
                                                                                            rpm=numbers_dict['rpm'],
                                                                                            tranny_gear=gear_ratios[-1],
                                                                                            tcase=transfercase_final_value,
                                                                                            diff=numbers_dict[
                                                                                                'differentialGearRatio'])))

    return 'Effective Tire Diameter is {} inches'.format(tire_diameter)


if __name__ == '__main__':
    app.run_server()
