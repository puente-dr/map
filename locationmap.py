# Dash packages
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# Graphing packages
import plotly.graph_objs as go
import plotly.express as px
from mapboxgl.utils import *
from mapboxgl.viz import *

# Other packages
import numpy as np
import pandas as pd
from statistics import *
from data_cleaning import script, maindataclean

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

df = maindataclean.clean_data()
df = df.dropna()


community_names = sorted(df['Community (Clean)'].unique())
city_names = sorted(df['City (Clean)'].unique())

all_location_options = ["City (Clean)","Community (Clean)"]


app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Graph(
                    id="display-selected-values",
                    figure={},
                    style={
                        "top": "0",
                        "left": "0",
                        "position": "fixed",
                        "width": "75%",
                    },
                )
            ],
            style={"width": "100%", "display": "table", "top": "0", "left": "0"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label(
                            [
                                "Location Level of Detail",
                                dcc.Dropdown(
                                    id="location-features-dropdown",
                                    options=[
                                        {"label": i, "value": i}
                                        for i in all_location_options
                                    ],
                                    value='Community (Clean)',
                                    style={"font-family": "Roboto"},
                                ),
                            ]
                        )
                    ],
                    style={"width": "100%"},
                ),
               html.Div(
                    [
                        html.Label(
                            [
                                "Location Selector",
                                dcc.Dropdown(
                                    id="location-options-dropdown",
                                    multi = False,
                                    value = 'Arenzano',
                                ),
                            ]
                        )
                    ],
                    style={"width": "100%"},
                ),
                html.Hr(),
            ],
            style={
                "width": "25%",
                "position": "fixed",
                "top": "1",
                "right": "0",
                "display": "table",
            },
        ),
    ],
    style={"top": "1", "left": "0"},
)

@app.callback(
    Output("location-options-dropdown", "options"), Input("location-features-dropdown", "value")
)
def set_location_options(location_selected_feature):
    dff = df
    dff = dff[dff[location_selected_feature] != ""]
    return [{"label": i.capitalize(), "value": i} for i in sorted(dff[location_selected_feature].unique())]


@app.callback(Output("location-options-dropdown", "value"), Input("location-options-dropdown", "options"))
def set_location_options_value(location_available_options):
    return location_available_options



@app.callback(
    Output("display-selected-values", "figure"),
    Input("location-features-dropdown", "value"),
    Input("location-options-dropdown", "value"),
)
def set_display_children(location_selected_feature, location_selected_option):
    token = os.getenv(
        "pk.eyJ1IjoibXN1YXJlejkiLCJhIjoiY2ttZ3F1cjZ0MDAxMjJubW5tN2RsYzI2bCJ9.l7Ht-cO4Owt7vgiAY3lwsQ"
    )
    px.set_mapbox_access_token(
        "pk.eyJ1IjoibXN1YXJlejkiLCJhIjoiY2ttZ3F1cjZ0MDAxMjJubW5tN2RsYzI2bCJ9.l7Ht-cO4Owt7vgiAY3lwsQ"
    )
    dff = df[df['Latitude']!=''] 
    dff = dff[dff[location_selected_feature] == (location_selected_option)]
    avg_lat = mean(dff["Latitude"])
    avg_lon = mean(dff["Longitude"])

    # dff = df[df['Roof Condition'].isin(value)]

    fig = px.scatter_mapbox(
        data_frame=dff,  # [df['Clinic Access']==value],
        lat=dff["Latitude"],
        lon=dff["Longitude"],
        # color_discrete_map={'Y':'green','N':'red','':'gray'},
        hover_name="Community (Clean)",
        hover_data={'Education Level':True,'Water Access':True,'Clinic Access':True,'Floor Condition':True,'Roof Condition':True,'Latrine or Bathroom Access':True,'Longitude':False,'Latitude':False},
        zoom=13,
    )

    fig.update_layout(
        autosize=True,
        # margins=dict{l:0},
        title="Dominican Republic Health Data by Household<br>(Hover over map for details)",
        title_font_family="Roboto",
        geo_scope="world",
        geo=dict(
            projection_scale=1000000,  # this is kind of like zoom
            center=dict(lat=avg_lat, lon=avg_lon),
        ),  # this will center on the point
    )
    fig.update_traces(hoverinfo="lon")
    fig.update_layout(mapbox_style="mapbox://styles/msuarez9/ckmp4rt7e0qf517o1md18w9d1")
    fig.update_layout(
        legend=dict(
            font_family="Roboto",
            orientation="h",
            yanchor="bottom",
            xanchor="left",
            y=-0.15,
            # width = '90%'
            # x=0
        ),
        hoverlabel=dict(bgcolor="white", font_size=16, font_family="Roboto"),
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)