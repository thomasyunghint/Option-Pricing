import dash_bootstrap_components as dbc
from dash import dcc, html
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, date
from plotly.subplots import make_subplots

from pages.options.functions import BSM_Greeks, get_vol_matrix
import numpy as np

op_type_select = dbc.Select(
    id="op_type_select",
    options=[
        {"label": "Call", "value": "call"},
        {"label": "Put", "value": "put"},
    ],
    value="call",
)

op_ticker_input = dbc.Input(id="op_ticker_input", placeholder="AAPL", type="text")
op_strike_input = dbc.Input(id="op_strike_input", placeholder=200, type="number")
op_exp_input = dcc.DatePickerSingle(id="op_exp_input", date=datetime.now().date())
op_submit_btn = dbc.Button("Submit", id="submit", n_clicks=0, style={"width": "100px"})


def get_chart(ticker):
    close = ticker.history(period="1mo").reset_index()
    fig = go.Figure([go.Scatter(x=close["Date"], y=close["Close"])])
    return fig


def get_greeks_plot(S: float, T: float, sigma: float, _type: str = "call"):
    greeks = BSM_Greeks()
    fig = make_subplots(
        rows=3,
        cols=2,
        start_cell="top-left",
        subplot_titles=("Delta", "Gamma", "Vega", "Theta", "Rho"),
    )
    K = np.arange(S * 0.5, S * 1.5)
    delta = [greeks.delta(S, k, sigma, T, _type) for k in K]
    gamma = [greeks.gamma(S, k, sigma, T) for k in K]
    vega = [greeks.vega(S, k, sigma, T) for k in K]
    theta = [greeks.theta(S, k, sigma, T) for k in K]
    rho = [greeks.theo(S, k, sigma, T, _type) for k in K]

    fig.add_trace(go.Scatter(x=K, y=delta, name="delta"), row=1, col=1)

    fig.add_trace(go.Scatter(x=K, y=gamma, name="gamma"), row=1, col=2)

    fig.add_trace(go.Scatter(x=K, y=vega, name="vega"), row=2, col=1)

    fig.add_trace(go.Scatter(x=K, y=theta, name="theta"), row=2, col=2)

    fig.add_trace(go.Scatter(x=K, y=rho, name="rho"), row=3, col=1)
    fig.update_layout(
        height=1000, width=1000, title_text=f"{_type.capitalize()} Option Greeks"
    )

    return fig

input_groups = html.Div(
    [
        dbc.InputGroup(
            [dbc.InputGroupText("Ticker"), op_ticker_input],
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Strike"),
                op_strike_input,
            ],
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Expiration"),
                op_exp_input,
            ]
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Type"),
                op_type_select,
            ],
        ),
    ],
    style={"width": "300px"},
)


def get_vol_plot(ticker):
    z_data = get_vol_matrix(ticker)
    z = z_data.values

    # x: strike labels
    x_strikes = z_data.index.values  # e.g., [150, 160, ..., 250]
    # y: expiration date labels
    y_expiries = list(z_data.columns)  # e.g., ['2024-04-19', '2024-04-26', ...]

    # Create meshgrid of x, y for surface plot
    import numpy as np

    x_mesh, y_mesh = np.meshgrid(x_strikes, range(len(y_expiries)))  # y is row index

    # Plotly surface with custom ticks
    fig = go.Figure(
        data=[go.Surface(z=z.T, x=x_strikes, y=list(range(len(y_expiries))))]
    )

    # Add labels and custom tick text
    fig.update_layout(
        title=dict(text="Implied Vol Surface"),
        autosize=False,
        width=1500,
        height=600,
        margin=dict(l=65, r=50, b=65, t=90),
        scene=dict(
            xaxis=dict(
                title="Strike Price",
                tickvals=list(x_strikes[::5]),  # every 5th strike
                ticktext=[str(s) for s in x_strikes[::5]],
            ),
            yaxis=dict(
                title="Expiration Date",
                tickvals=list(range(len(y_expiries))),  # expiration indices
                ticktext=y_expiries,  # actual date labels
            ),
            zaxis=dict(title="Implied Volatility"),
            aspectratio=dict(x=1, y=2, z=0.7),
        ),
    )

    return fig

