import requests
import pandas as pd
import requests
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

#Survey df
url = 'http://flask-api-layer-env.eba-tpsx3zvp.us-east-1.elasticbeanstalk.com/records'
results=requests.get(url)
json = results.json()
api_survey_df = pd.DataFrame(json['records'])
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Textarea(
        id='textarea-example',
        value='The length of the survey df is {}'.format(len(api_survey_df)),
        style={'width': '100%', 'height': 200},
    ),
    html.Div(id='textarea-example-output', style={'whiteSpace': 'pre-line'})
])

@app.callback(
    Output('textarea-example-output', 'children'),
    Input('textarea-example', 'value')
)
def update_output(value):
    return 'The length of the survey data is: \n{}'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)