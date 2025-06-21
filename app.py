import dash
import dash_bootstrap_components as dbc
from components.header import navbar

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

app.layout = dbc.Container(
    [
        navbar,
        dash.page_container,
    ],
    fluid=True,
)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5050)

