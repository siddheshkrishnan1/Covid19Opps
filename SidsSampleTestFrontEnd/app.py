import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

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
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)