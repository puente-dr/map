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
from data_cleaning import script, maindataclean

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
    'Roof Condition':['Adequate', 'Needs Repair'],
    'Latrine or Bathroom Access':['Yes','No']
}

#import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,300;1,400;1,500;1,700&display=swap')

app.layout = html.Div([
    html.Div([
        dcc.Graph(id='display-selected-values',figure={},style={'top':'0','left':'0','position':'fixed','width':'75%'})
        ],style={'width':'100%','display':'table','top':'0','left':'0'}),
    
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

    ],style={'width':'25%','position':'fixed', 'top':'1','right':'0','display':'table'}),

  ], style={'top':'1','left':'0'})
# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True

# external_css = [
#     "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",
#     "//fonts.googleapis.com/css?family=Roboto|Lato",
#     'https://codepen.io/chriddyp/pen/bWLwgP.css',
# ]

# for css in external_css:
#     app.css.append_css({"external_url": css})
 
#@import {}
# @font-face {
#   font-family: 'Roboto';
#   font-style: normal;
#   font-weight: 400;
#   src: local('Roboto'), local('Roboto-Regular'), url(https://fonts.gstatic.com/s/roboto/v18/KFOmCnqEu92Fr1Mu4mxK.woff2) format('woff2');
#   unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
# }

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
    token = os.getenv('pk.eyJ1IjoibXN1YXJlejkiLCJhIjoiY2ttZ3F1cjZ0MDAxMjJubW5tN2RsYzI2bCJ9.l7Ht-cO4Owt7vgiAY3lwsQ')
    px.set_mapbox_access_token('pk.eyJ1IjoibXN1YXJlejkiLCJhIjoiY2ttZ3F1cjZ0MDAxMjJubW5tN2RsYzI2bCJ9.l7Ht-cO4Owt7vgiAY3lwsQ')
    
    
    if selected_option == []:
        dff = df[df['City (Clean)']==selected_city]
        avg_lat = mean(dff['Latitude'])
        avg_lon = mean(dff['Longitude'])

        fig = px.scatter_mapbox(
            data_frame = dff, #[df['Clinic Access']==value],
            lat = dff['Latitude'], 
            lon = dff['Longitude'],
            zoom = 13,
            hover_data={'Latitude':False,'Longitude':False},
        )
        fig.update_traces(marker_opacity=0)

    else:
        dff = df[df[selected_feature].isin(selected_option)]
        dff = dff[dff['City (Clean)']==selected_city]
        avg_lat = mean(dff['Latitude'])
        avg_lon = mean(dff['Longitude'])

        #dff = df[df['Roof Condition'].isin(value)]
    
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
        autosize=True,
        #margins=dict{l:0},
        title = 'Dominican Republic Health Data by Household<br>(Hover over map for details)',
        title_font_family='Roboto',
        geo_scope='world',
            geo = dict(
            projection_scale=1000000, #this is kind of like zoom
            center=dict(lat = avg_lat,lon=avg_lon)) # this will center on the point
    )
    fig.update_traces(hoverinfo='lon')
    fig.update_layout(mapbox_style="mapbox://styles/msuarez9/ckmp4rt7e0qf517o1md18w9d1")
    fig.update_layout(
        legend=dict(
            font_family='Roboto',
            orientation="h",
            yanchor="bottom",
            xanchor="left",
            y=-.15,
            #width = '90%'
            #x=0
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Roboto"
        )
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)