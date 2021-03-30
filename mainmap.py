#Dash packages
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

#Graphing packages
import plotly.graph_objs as go
import plotly.express as px
from mapboxgl.utils import *
from mapboxgl.viz import *

#Other packages
import numpy as np
import pandas as pd
from statistics import *
#from Data_Cleaning import script
from Data_Cleaning import maindataclean

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
df = maindataclean.clean_data()
df = df.dropna()

all_options = {
    'Education Level': ['Less Than Primary School', 'Completed Primary School', 'Completed College',
 'Completed High School', 'Some High School',  'Some College'],
    'Water Access': ['2-3x A Week', '4-6x A Week', '1x A Month', 'Never', '1x A Week', 'Every day'],
    'Clinic Access':['Yes', 'No'],
    'Floor Condition':['Great', 'Needs Repair', 'Adequate'],
    'Roof Condition':['Adequate', 'Needs Repair']
}

#import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,300;1,400;1,500;1,700&display=swap')

app.layout = html.Div([
    html.Div([
        dcc.Graph(id='display-selected-values',figure={})
        ],style={'width':'60%','display':'inline-block','margin-left':'auto','margin-right':'0'}),
    
    html.Div([
        html.Div([
            html.Label(["City",
                dcc.Dropdown(
                    id = 'city-selection',
                    options=[{'label': x.capitalize(), 'value': x} for x in sorted(df['City (Clean)'].unique())],value='Constanza')]),
        ],style={'width':'100%'}),
        html.Div([
            html.Label(['Health Feature', 
                dcc.Dropdown(
                    id='features-dropdown',
                    options=[{'label': k, 'value': k} for k in all_options.keys()],
                    value='Education Level',
                    style={'font-family':'Roboto'}
                )
            ]),
        ], style={'width':'100%'}),

        html.Hr(),
        html.Div([
            html.Label(["Multiselect Feature Status",dcc.Dropdown(id='options-dropdown',
            multi=True,
            #font_family=('Roboto',sans-serif),
            #style={'size':'20%'},
            value=['Less Than Primary School', 'Completed Primary School', 'Completed College',
    'Completed High School', 'Some High School',  'Some College']
            )])
        ],style={'width':'100%'}),

        html.Hr(),

    ],style={'width':'35%','display':'inline-block','margin-left':'0','margin-right':'auto'}),

  ])


@app.callback(
    Output('options-dropdown', 'options'),
    Input('features-dropdown', 'value'))
def set_cities_options(selected_feature):
    dff = df
    dff = dff[dff[selected_feature]!='']
    return [{'label': i, 'value': i} for i in all_options[selected_feature]]


@app.callback(
    Output('options-dropdown', 'value'),
    Input('options-dropdown', 'options'))
def set_options_value(available_options):
    return [available_options[i]['value'] for i in range(len(available_options))]


@app.callback(
    Output('display-selected-values', 'figure'),
    Input('features-dropdown', 'value'),
    Input('options-dropdown', 'value'),
    Input('city-selection','value'))

def set_display_children(selected_feature, selected_option,selected_city):
    dff = df[df[selected_feature].isin(selected_option)]
    dff = dff[dff['City (Clean)']==selected_city]
    #dff = df[df['Roof Condition'].isin(value)]
    token = os.getenv('pk.eyJ1IjoibXN1YXJlejkiLCJhIjoiY2ttZ3F1cjZ0MDAxMjJubW5tN2RsYzI2bCJ9.l7Ht-cO4Owt7vgiAY3lwsQ')
    px.set_mapbox_access_token('pk.eyJ1IjoibXN1YXJlejkiLCJhIjoiY2ttZ3F1cjZ0MDAxMjJubW5tN2RsYzI2bCJ9.l7Ht-cO4Owt7vgiAY3lwsQ')
    fig = px.scatter_mapbox(
        data_frame = dff, #[df['Clinic Access']==value],
        lat = dff['Latitude'], 
        lon = dff['Longitude'],
        color = dff[selected_feature],
        #color_discrete_map={'Y':'green','N':'red','':'gray'},
        hover_name="Community (Clean)",
        hover_data={'Latitude':False,'Longitude':False},
        zoom = 13
    )


    fig.update_layout(
        title = 'Dominican Republic Health Data by Household<br>(Hover over map for details)',
        geo_scope='world',
            geo = dict(
            projection_scale=1000000, #this is kind of like zoom
            center=dict(lat = mean(dff['Latitude']),lon=mean(dff['Longitude'])) # this will center on the point
    ))
    fig.update_traces(hoverinfo='lon')
    fig.update_layout(mapbox_style="mapbox://styles/msuarez9/ckmp4rt7e0qf517o1md18w9d1")
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Roboto"
        )
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)