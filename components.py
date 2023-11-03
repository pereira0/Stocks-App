import dash_bootstrap_components as dbc
import dash_html_components as html
import data_cleanup

dropdown = dbc.DropdownMenu(
    label="Suppliers",
    menu_variant="dark",
    children=[
        dbc.DropdownMenuItem("Opadipity"),
        dbc.DropdownMenuItem("Triscuits"),
        dbc.DropdownMenuItem("Califia"),
    ],
    className="d-grid gap-2 d-md-flex justify-content-md-end",
    align_end=True
)


# CARDS
def create_display_cards(current_stocks_d, period_sales_d):
    current_stocks_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(current_stocks_d, className="card-title"),
                    html.H6("Current stocks", className="card-subtitle"),
                ]
            ),
            style={"width": "18rem"},
        )

    period_sales_card = dbc.Card(
        dbc.CardBody(
            [
                html.H4(period_sales_d, className="card-title"),
                html.H6("Period sales", className="card-subtitle"),
            ]
        ),
        style={"width": "18rem"},
    )

    return current_stocks_card, period_sales_card
