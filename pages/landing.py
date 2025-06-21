import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc


dash.register_page(__name__, title="Home", name="Home", path="/")


layout = html.Div(
    ["This is Landing Page"], className="page-container")

