from dash import Dash
from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div(id='target', style={'fontFamily': 'Roboto'}),
    dcc.Input(id='input',style={'fontFamily':'Roboto'}, type='text', value=''),
    html.Button(id='submit', style={'fontFamily':'Roboto'},n_clicks=0, children='Save')
])

body {
    font-family:'Roboto',sans-serif
}
#@font-face {}
#@import url('https://fonts.googleapis.com/css?family=Noto+Sans&display=swap')

# }
# external_css = [
#     "//fonts.googleapis.com/css?family=Roboto"]

# for css in external_css:
#     app.css.append_css({"external_url": css})


@app.callback(Output('target', 'children'), [Input('submit', 'n_clicks')],
              [State('input', 'value')])
def callback(n_clicks, state):
    return "callback received value: {}".format(state)


if __name__ == '__main__':
    app.run_server(debug=True)