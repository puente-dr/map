# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from data_cleaning import script, maindataclean

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


df = maindataclean.clean_data()
df['Community (Clean)'] = df['Community (Clean)'].fillna(9999)
df['City (Clean)'] = df['City (Clean)'].fillna(9999)


community_names = []
city_names = []
for x in df['Community (Clean)'].unique():
    community_names.append(x)

for x in df['City (Clean)'].unique():
    city_names.append(x)

all_options = {"City (Clean)":city_names,"Community (Clean)":community_names}


app.layout = html.Div([
    dcc.RadioItems(
        id='countries-radio',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='City (Clean)'
    ),

    html.Hr(),

    dcc.RadioItems(id='cities-radio'),

    html.Hr(),

    html.Div(id='display-selected-values')
])


@app.callback(
    Output('cities-radio', 'options'),
    Input('countries-radio', 'value'))
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]


@app.callback(
    Output('cities-radio', 'value'),
    Input('cities-radio', 'options'))
def set_cities_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('display-selected-values', 'children'),
    Input('countries-radio', 'value'),
    Input('cities-radio', 'value'))
def set_display_children(selected_country, selected_city):
    return u'{} is a city in {}'.format(
        selected_city, selected_country,
    )


if __name__ == '__main__':
    app.run_server(debug=True)