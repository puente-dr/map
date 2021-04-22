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
from data_cleaning import maindataclean

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

df = maindataclean.clean_data()
proj_df = pd.read_excel(
        "data/Puente Project Tracker 1-8.xlsx", sheet_name="MapCommunities"
    )

# Remove Tireo bc no information on it in the current data frame
city_names = sorted(df["City"].dropna().unique().tolist())
# city_names.remove('Tireo')

# Community names for map
community_focus = [
    "Los Gajitos",
    "El Canal",
    "Cañada las Palmas",
    "El Convento",
    "Los Embassadores",
    "Los Mangos",
    "Cuidad de Dios",
]
community_names = community_focus
df = df[df["Community"].isin(community_focus)]

# Map
all_location_options = {"City": city_names, "Community": community_names}
all_health_options = {
    "Clinic Access": ["Yes", "No"],
    "Water Access": [
        "Every day",
        "4-6x A Week",
        "2-3x A Week",
        "1x A Week",
        "1x A Month",
        "Never",
    ],
    "Floor Condition": ["Good", "Adequate", "Needs Repair"],
    "Roof Condition": ["Adequate", "Needs Repair"],
    "Latrine or Bathroom Access": ["Yes", "No"],
}

color_map = {
    "Clinic Access": {"Yes": "#016930", "No": "#03CA5D"},
    "Water Access": {
        "Every day": "#013856",
        "4-6x A Week": "#016ca0",
        "2-3x A Week": "#0099dc",
        "1x A Week": "#85e8ff",
        "1x A Month": "#cef6fe",
        "Never": "#f3fdff",
    },
    "Floor Condition": {
        "Good": "#23015B",
        "Adequate": "#9E63FF",
        "Needs Repair": "#CFB2FE",
    },
    "Roof Condition": {"Adequate": "#dd8b01", "Needs Repair": "#fdc475"},
    "Latrine or Bathroom Access": {"Yes": "#740702", "No": "#f78a78"},
}

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    dcc.Graph(
                        id="display-selected-values",
                        figure={},
                        style={
                            # This controls the Map Div
                            "height": "800px"
                        },
                    )
                )
            ],
            style={
                # This controls the Map Container Div
                "background-color": "#f8f7f6",
                "flex": "2 0 0",
            },
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            html.Label("Geographic Level of Detail"),
                            style={"font-family": "Roboto", "font-weight": "bold"},
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="location-features-dropdown",
                                    options=[
                                        {"label": k, "value": k}
                                        for k in all_location_options.keys()
                                    ],
                                    value="Community",
                                    style={"font-family": "Roboto"},
                                )
                            ]
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Div(
                            html.Label("Select Location..."),
                            style={"font-family": "Roboto", "font-weight": "bold"},
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="location-options-dropdown",
                                    multi=False,
                                    value="Los Gajitos",
                                )
                            ]
                        ),
                    ],
                    style={"width": "100%"},
                ),
                html.Hr(style={"margin-top": "20px","margin-bottom":"20px"}),
                html.Div(
                    [
                        html.Div(
                            html.Label("Household Features"),
                            style={"font-family": "Roboto", "font-weight": "bold"},
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="health-features-dropdown",
                                    options=[
                                        {"label": k, "value": k}
                                        for k in all_health_options.keys()
                                    ],
                                    value="Clinic Access",
                                    style={"font-family": "Roboto"},
                                )
                            ]
                        ),
                    ],
                    style={"width": "100%"},
                ),
                html.Div(
                    [
                        html.Div(
                            html.Label("Select Features..."),
                            style={"font-family": "Roboto", "font-weight": "bold"},
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="health-options-dropdown",
                                    multi=True,
                                    clearable=False,
                                    # font_family=('Roboto',sans-serif),
                                    # style={'size':'20%'},
                                    value=["Yes", "No"],
                                )
                            ]
                        ),
                    ],
                    style={"width": "100%"},
                    className="custom-dropdown",
                ),
                html.Div(
                    id="dd-output-container",
                    style={"font-family": "Roboto", "font-size": "20px"},
                ),
            ],
            style={
                # This controls the Features Table Div
                "background-color": "#f8f7f6",
                "flex": "1 0 0",
            },
        ),
    ],
    style={
        # This controls the Div for the Entire Visualization
        "display": "flex",
        "flex-direction": "row",
        "background-color": "#f8f7f6",
    },
)


@app.callback(
    Output("location-options-dropdown", "options"),
    Input("location-features-dropdown", "value"),
)
def set_location_options(location_selected_feature):
    dff = df
    dff = dff[dff[location_selected_feature] != ""]
    return [
        {"label": i, "value": i}
        for i in all_location_options[location_selected_feature]
    ]


@app.callback(
    Output("location-options-dropdown", "value"),
    Input("location-options-dropdown", "options"),
)
def set_location_options_value(location_available_options):
    return location_available_options[0]["value"]

@app.callback(
    Output("health-options-dropdown", "options"),
    Input("health-features-dropdown", "value"),
)
def set_health_options(health_selected_feature):
    dff = df
    dff = dff[dff[health_selected_feature] != ""]
    return [
        {"label": i, "value": i} for i in all_health_options[health_selected_feature]
    ]


@app.callback(
    Output("health-options-dropdown", "value"),
    Input("health-options-dropdown", "options"),
)
def set_health_options_value(health_available_options):
    return [
        health_available_options[i]["value"]
        for i in range(len(health_available_options))
    ]


# @app.callback(
#     Output('dd-output2-container', 'children'),
#     Input("location-features-dropdown", "value"),)
# def update_output2(location_features):
#     return "Hi thi is {}".format(location_features)


@app.callback(
    Output("dd-output-container", "children"),
    Input("location-features-dropdown", "value"),
    Input("location-options-dropdown", "value"),
    Input("health-features-dropdown", "value"),
    Input("health-options-dropdown", "value"),
)
def update_output(
    location_selected_feature,
    location_selected_option,
    health_selected_feature,
    health_selected_option,
):
    dff = df[df[health_selected_feature] != ""]
    dff = dff[dff[location_selected_feature].isin([location_selected_option])]
    if health_selected_feature == "Clinic Access":
        num = len(dff[dff["Clinic Access"] == "No"]) / len(dff)
        percentage = "{:.0%}".format(num)
        return "In {}, {} of housholds do not have access to clinics".format(
            location_selected_option, percentage
        )
    if health_selected_feature == "Water Access":
        num = len(
            dff[dff["Water Access"].isin(["1x A Month", "Never", "1x A Week"])]
        ) / len(dff)
        percentage = "{:.0%}".format(num)
        if location_selected_option in proj_df['Community'].unique():
            water_filters = proj_df.loc[proj_df['Community']==location_selected_option,'Water Filters'].iloc[0]
        else:
            water_filters = 0
        if water_filters >0:
            return "In {}, {} of housholds have inadequate access to water. \n\n Puente has distributed {} water filters in this community.".format(
            location_selected_option, percentage,water_filters
            )
        else:
            return "In {}, {} of housholds have inadequate access to water".format(
                location_selected_option, percentage
            )
    if health_selected_feature == "Floor Condition":
        num = len(dff[dff["Floor Condition"] == "Needs Repair"]) / len(dff)
        percentage = "{:.0%}".format(num)
        if location_selected_option in proj_df['Community'].unique():
            floors = proj_df.loc[proj_df['Community']==location_selected_option,'Floors'].iloc[0]
        else:
            floors = 0
        if floors> 0:
            return ("In {}, {} of housholds need flooring repairs.".format(location_selected_option, percentage) + "\n"+"Puente has helped repair {} floors in this community.".format(
            floors
            ))
        else:
            return "In {}, {} of housholds need flooring repairs".format(
                location_selected_option, percentage
            )
    if health_selected_feature == "Roof Condition":
        num = len(dff[dff["Roof Condition"] == "Needs Repair"]) / len(dff)
        percentage = "{:.0%}".format(num)
        return "In {}, {} of housholds need roof repairs".format(
            location_selected_option, percentage
        )
    if health_selected_feature == "Latrine or Bathroom Access":
        num = len(dff[dff["Latrine or Bathroom Access"] == "No"]) / len(dff)
        percentage = "{:.0%}".format(num)
        if location_selected_option in proj_df['Community'].unique():
            bathrooms = proj_df.loc[proj_df['Community']==location_selected_option,'Bathrooms'].iloc[0]
        else:
            bathrooms = 0
        if  bathroomes > 0:
            return "In {}, {} of housholds do not have access to latrines or bathrooms.\n\nPuente has helped install {} bathrooms in this community.".format(
            location_selected_option, percentage,bathrooms
            )
        else:
            return "In {}, {} of housholds do not have access to latrines or bathrooms. \n \n ".format(
            location_selected_option, percentage
            )

    # else if health_feature == 'Water Access':
    # else if health_feature == 'Floor Condition':
    # else if health_feature == 'Roof Condition':
    # else if health_feature == 'Latrine or Bathroom Access':
    #     return 'In {}, {} of housholds do not have access to clinics".format(location_value)


@app.callback(
    Output("display-selected-values", "figure"),
    Input("location-features-dropdown", "value"),
    Input("location-options-dropdown", "value"),
    Input("health-features-dropdown", "value"),
    Input("health-options-dropdown", "value"),
)
def set_display_children(
    location_selected_feature,
    location_selected_option,
    health_selected_feature,
    health_selected_option,
):
    token = os.getenv(
        "pk.eyJ1IjoibXN1YXJlejkiLCJhIjoiY2ttZ3F1cjZ0MDAxMjJubW5tN2RsYzI2bCJ9.l7Ht-cO4Owt7vgiAY3lwsQ"
    )
    px.set_mapbox_access_token(
        "pk.eyJ1IjoibXN1YXJlejkiLCJhIjoiY2ttZ3F1cjZ0MDAxMjJubW5tN2RsYzI2bCJ9.l7Ht-cO4Owt7vgiAY3lwsQ"
    )

    dff = df[df[location_selected_feature] == location_selected_option]
    avg_lat = mean(dff["Latitude"])
    avg_lon = mean(dff["Longitude"])

    if (
        health_selected_option == []
        or len(dff[dff[health_selected_feature].isin(health_selected_option)]) == 0
    ):
        fig = px.scatter_mapbox(
            bgcolor="#f8f7f6",
            data_frame=dff,  # [df['Clinic Access']==value],
            lat=dff["Latitude"],
            lon=dff["Longitude"],
            zoom=15,
            hover_data={
                "Water Access": False,
                "Clinic Access": False,
                "Floor Condition": False,
                "Roof Condition": False,
                "Latrine or Bathroom Access": False,
                "Longitude": False,
                "Latitude": False,
            },
        )
        fig.update_traces(marker_opacity=0)

    else:
        dff = dff[dff[health_selected_feature].isin(health_selected_option)]
        lat_val = dff["Latitude"]
        lon_val = dff["Longitude"]
        fig = px.scatter_mapbox(
            data_frame=dff,  # [df['Clinic Access']==value],
            lat=dff["Latitude"],
            lon=dff["Longitude"],
            color=dff[health_selected_feature],
            color_discrete_map=color_map[health_selected_feature],
            hover_name="Community",
            hover_data={
                "Water Access": True,
                "Clinic Access": True,
                "Floor Condition": True,
                "Roof Condition": True,
                "Latrine or Bathroom Access": True,
                "Longitude": False,
                "Latitude": False,
            },
            zoom=15,
            opacity=0.8,
            category_orders={
                health_selected_feature: all_health_options[health_selected_feature]
            },
            custom_data=[
                "Community",
                "Water Access",
                "Clinic Access",
                "Floor Condition",
                "Roof Condition",
                "Latrine or Bathroom Access",
            ],
        )
        # fig.update_traces(
        #     hoverinfo="lon",
        #     hovertemplate="<span style='font-size:20px'><b>%{customdata[0]}</b> </span><br> <br> <b>Water Access:</b> %{customdata[1]}<br> <b>Clinic Access:</b> %{customdata[2]}<br> <b>Floor Condition:</b> %{customdata[3]}<br> <b>Roof Condition:</b> %{customdata[4]}<br> <b>Latrine or Bathroom Access:</b> %{customdata[5]}",
        # )
        fig.update_traces(marker_size=15)  # ids='123test',
        # fig.add_trace(go.Scattermapbox(
        #     lat=lat_val,
        #     lon=lon_val,
        #     mode='markers',
        #     marker=go.scattermapbox.Marker(color='grey',
        #         #below='123test',
        #         allowoverlap=False,
        #         size=18,
        #         opacity=0.4
        #         ),
        # hoverinfo='none',
        # #coloraxis_showscale=False
        # ))
        fig.update_layout(
            hoverlabel=dict(bgcolor="white", font_size=16, font_family="Roboto")
        )
        fig.update_traces(#ids='123test',
        marker_size=15)
        # fig.add_trace(go.Scattermapbox(
        #     lat=lat_val,
        #     lon=lon_val,
        #     mode='markers',
        #     marker=go.scattermapbox.Marker(color='grey',
        #         #below='123test',
        #         allowoverlap=False,
        #         size=18,
        #         opacity=0.4
        #         ),
        # hoverinfo='none',
        # #coloraxis_showscale=False
        # ))
        fig.update_layout(hoverlabel=dict(bgcolor="white", font_size=16, font_family="Roboto"))



    fig.update_layout(
        autosize=True,
        # margins=dict{l:0},
        title="<b>Dominican Republic Health Data by Household</b><br>(Hover over map for details)",
        title_font_family="Roboto",
        font_family="Roboto",
        geo_scope="world",
        geo=dict(
            projection_scale=1000000,  # this is kind of like zoom
            center=dict(lat=avg_lat, lon=avg_lon),
        ),  # this will center on the point
    )

    fig.update_layout(mapbox_style="mapbox://styles/msuarez9/ckmp4rt7e0qf517o1md18w9d1")
    fig.update_layout(
        legend_title=dict(font=dict(family="Roboto", size=20, color="black")),
        legend=dict(
            font_family="Roboto",
            font=dict(family="Roboto", size=18, color="black"),
            orientation="h",
            yanchor="bottom",
            xanchor="left",
            y=-0.09,
            # width = '90%'
            # x=0
        ),
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
