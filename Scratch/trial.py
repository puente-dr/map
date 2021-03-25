import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

all_options = {
    'Education Level': ['Less Than Primary School', 'Completed Primary School', 'Completed College',
 'Completed High School', 'Some High School', '', 'Some College'],
    'Water Access': ['2-3x A Week', '4-6x A Week', '1x A Month', 'Never', '1x A Week', 'Every day',
 ''],
    'Clinic Access':['Yes', 'No', ''],
    'Floor Condition':['Great', 'Needs Repair', 'Adequate', ''],
    'Roof Condition':['Adequate', 'Needs Repair', '']
}

app.layout = html.Div([
    dcc.Dropdown(
        id='features-dropdown',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='Education Level'
    ),

    html.Hr(),

    dcc.Dropdown(id='options-dropdown',value=['Less Than Primary School', 'Completed Primary School', 'Completed College',
 'Completed High School', 'Some High School', '', 'Some College'],multi=True),

    html.Hr(),

    html.Div(id='display-selected-values')
])


@app.callback(
    Output('options-dropdown', 'options'),
    Input('features-dropdown', 'value'))
def set_cities_options(selected_feature):
    return [{'label': i, 'value': i} for i in all_options[selected_feature]]


@app.callback(
    Output('options-dropdown', 'value'),
    Input('options-dropdown', 'options'))
def set_cities_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('display-selected-values', 'children'),
    Input('features-dropdown', 'value'),
    Input('options-dropdown', 'value'))
def set_display_children(selected_option, selected_feature):
    return u'You are viewing households with {} for the feature: {}'.format(
        selected_feature, selected_option,
    )


if __name__ == '__main__':
    app.run_server(debug=True)