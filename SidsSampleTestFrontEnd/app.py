import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


app = dash.Dash()

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

app.layout = html.Div(children=[
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



if __name__ == '__main__':
    app.run_server(debug=True)