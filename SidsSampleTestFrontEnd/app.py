import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Click here if you are bored", className="card-title"),
                html.P(
                    "Card-text ",
                    className="card-text",
                ),
                dbc.Button("Boreddd", color="primary"),
            ]
        ),
    ],
    style={"width": "18rem"},
)


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Tab one', value='tab-1'),
        dcc.Tab(label='Tab two', value='tab-2'),
    ]),
    html.Div(id='tabs-example-content')
])


valA = html.Div(children=[
    html.H1(children='My Boredom in Quarentine'),
        dcc.Graph(
        id='example',
        figure={
            'data': [
                {'x': [1, 2, 3, 4, 5], 'y': [1, 2, 4, 8, 16], 'type': 'line', 'name': 'Boredom'},
                {'x': [1, 2, 3, 4, 5], 'y': [16, 8, 4, 2, 1], 'type': 'bar', 'name': 'Fun'},
            ],
            'layout': {
                'title': 'Boredom'
            }
        }
    ),
    dbc.Row([
        dbc.Col([card]), dbc.Col([card])
    ])])


@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return valA
    elif tab == 'tab-2':
        return html.Div([
            html.H3('More stuff here')
        ])


if __name__ == '__main__':
    app.run_server(debug=True)

