import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import dcc

import assets.styles
import data_cleanup


# supplier dropdown
def create_dropdown_supplier_selector(list_of_suppliers_d):
    dropdown = dcc.Dropdown(list_of_suppliers_d, list_of_suppliers_d[0], clearable=False, id='dropdown-button')

    return dropdown


# CARDS
def create_display_cards(current_stocks_d, period_sales_d, stock_ratio_d, unique_stock_refs_d, unique_sales_refs_d, stockout_ref_count_d):
    current_stocks_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(current_stocks_d, className="card-title"),
                    html.H6("Current stocks", className="card-subtitle"),
                ]
            ),
        )

    period_sales_card = dbc.Card(
        dbc.CardBody(
                [
                    html.H4(period_sales_d, className="card-title"),
                    html.H6("Period sales", className="card-subtitle"),
                ]
            ),
        )

    stock_ratio_card = dbc.Card(
        dbc.CardBody(
                [
                    html.H4(stock_ratio_d, className="card-title"),
                    html.H6("Stock Ratio", className="card-subtitle"),
                ]
            ),
        )

    unique_stock_refs_card = dbc.Card(
        dbc.CardBody(
                [
                    html.H4(unique_stock_refs_d, className="card-title"),
                    html.H6("Number of SKUs", className="card-subtitle"),
                ]
            ),
        )

    unique_sales_refs_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(unique_sales_refs_d, className="card-title"),
                    html.H6("Unique Products Sold", className="card-subtitle"),
                ]
            ),
        )

    stockout_ref_count_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(stockout_ref_count_d, className="card-title"),
                    html.H6("Stockout Risk Count", className="card-subtitle"),
                ]
            ),
        )

    return current_stocks_card, period_sales_card, stock_ratio_card, unique_stock_refs_card, unique_sales_refs_card, stockout_ref_count_card


# SIDEBAR
sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=assets.styles.SIDEBAR_STYLE,
)
