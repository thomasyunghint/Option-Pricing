import dash
import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Options", href="/options"),
                dbc.DropdownMenuItem("Project 2", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="Projects",
        ),
    ],
    brand="My Website",
    dark=True,
    id="header",
)
