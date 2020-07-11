from flask import Flask
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html


server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname='/first-app'
)

app.layout = html.Div(id='dash-container')

@server.route("/first-app")
def my_app():
    return app.index()