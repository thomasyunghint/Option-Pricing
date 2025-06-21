import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, callback, ctx, no_update
import yfinance as yf
import time
from pages.options.components import (
    input_groups,
    op_submit_btn,
    get_chart,
    get_greeks_plot,
    get_vol_plot,
)

from pages.options.functions import bs_formula, get_r, get_last_price, get_sigma
from datetime import date, datetime
import time


dash.register_page(
    __name__, path="/options", title="Option Analytics", name="Option Analytics"
)


_layout = html.Div(
    [
        dbc.Row("Option Pricer", id="option_price_header"),
        dbc.Row(input_groups),
        dbc.Row(op_submit_btn),
        dcc.Loading(
            [
                dbc.Row(id="option_price"),
                dbc.Row(html.Div(dcc.Graph(id="stock_chart"))),
                dbc.Row(html.Div(dcc.Graph(id="greeks_chart"))),
                dbc.Row(html.Div(dcc.Graph(id="vol_chart"))),
            ],
            overlay_style={
                "visibility": "visible",
                "opacity": 0.5,
                "backgroundColor": "white",
            },
            custom_spinner=dbc.Spinner(color="danger"),
        ),
    ],
    id="option_pricer",
    style={"padding": "100px"},
    className="page-container",
)


def layout():
    return _layout


@callback(
    Output(component_id="option_price", component_property="children"),
    Output(component_id="stock_chart", component_property="figure"),
    Output(component_id="greeks_chart", component_property="figure"),
    Output(component_id="vol_chart", component_property="figure"),
    Input(component_id="submit", component_property="n_clicks"),
    State("op_ticker_input", "value"),
    State("op_strike_input", "value"),
    State("op_exp_input", "date"),
    State("op_type_select", "value"),
)
def price_option(n_clicks, ticker, strike, exp_date, option_type):
    if ctx.triggered_id != "submit":
        return no_update, no_update, no_update, no_update

    if None in [ticker, strike, exp_date, option_type]:
        return "Invalid input!", no_update, no_update, no_update

    if (datetime.strptime(exp_date, "%Y-%m-%d") - datetime.today()).days <= 0:
        return "Invalid Date!", no_update, no_update, no_update

    ticker = yf.Ticker(ticker)
    S = get_last_price(ticker)
    sigma = get_sigma(ticker)
    T = (datetime.strptime(exp_date, "%Y-%m-%d") - datetime.today()).days / 365
    price = bs_formula(S, strike, T, sigma, option_type)
    fig = get_chart(ticker)
    fig_greeks = get_greeks_plot(S, T, sigma, option_type)
    fig_vol = get_vol_plot(ticker)
    return price, fig, fig_greeks, fig_vol
