import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

from data.data_cleaning import clean_api_code

dataframe = clean_api_code()

fig = px.scatter_mapbox(dataframe, lat="Latitude", lon="Longitude", hover_name="Water Access", hover_data=["Water Access", "Electricity Access"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=800)
fig.update_mapboxes(style='open-street-map')

app = dash.Dash()
# app.layout = html.Div([
#     dcc.Graph(figure=fig)
# ])

app.layout = html.Div([html.Div([html.H1("Puente Insights")],
                                style={'textAlign': "center"}
                               ),
                       dcc.Dropdown(id="value_selected", 
                                              options=[{'label': "Yes", 'value': 'Y'},
                                                       {'label': "No", 'value': 'N'}],
                                              multi = True,
                                              value = 'Y',
                                              style={"width": "40%"}
                                              ),
                       
              html.Div(id='output_container', children=[]),
              html.Br(),
                       
              dcc.Graph(id='my_puente_map',figure=fig)
              ])

app.run_server(debug=True, use_reloader=False)

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app.title = 'Puente Map'


# app.layout = html.Div([html.Div([html.H1("Puente Insights")],
#                                 style={'textAlign': "center"}
#                                ),
#                        dcc.Dropdown(id="value_selected", 
#                                               options=[{'label': "Yes", 'value': 'Y'},
#                                                        {'label': "No", 'value': 'N'}],
#                                               multi = True,
#                                               value = 'Y',
#                                               style={"width": "40%"}
#                                               ),
                       
#               html.Div(id='output_container', children=[]),
#               html.Br(),
                       
#               dcc.Graph(id='my_puente_map',figure={})
#               ])

# @app.callback(
#      [Output(component_id='output_container',component_property='children'),
#      Output(component_id='my_puente_map',component_property='figure')],
#      Input(component_id = 'value_selected',component_property='value')
# )
# def update_figure(selected):
#     dff = clean_api_code()

#     fig = px.scatter_geo(
#         data_frame = dff,
#         lat = dff['Latitude'], 
#         lon = dff['Longitude'],
#         hover_data = ['City']
#     )
#     return fig

# if __name__ == '__main__':
#     app.run_server(debug=True)