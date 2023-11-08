import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import dcc
import assets.styles as styles
import assets.text_translations as txt


# supplier dropdown
def create_dropdown_supplier_selector(list_of_suppliers_d):
    dropdown = dcc.Dropdown(list_of_suppliers_d, list_of_suppliers_d[0], clearable=False, id='dropdown-button')

    return dropdown


# CARDS
# set style for cards
def card_styling(value_d, text_d):
    generated_card = dbc.Card(
        dbc.CardBody(
            [
                html.P(text_d, className="card-subtitle", style={'color': styles.main_blue}),
                html.H3(value_d, className="card-title", style={'color': styles.main_blue}),
            ]
        ),
        style=styles.CARD_STYLE
    )

    return generated_card


# get cards for supplier stock tracker
def create_display_cards(current_stocks_d, period_sales_d, stock_ratio_d, unique_stock_refs_d, unique_sales_refs_d, stockout_ref_count_d):
    current_stocks_card = card_styling(current_stocks_d, txt.current_stocks)
    period_sales_card = card_styling(period_sales_d, txt.cogs_txt)
    stock_ratio_card = card_styling(stock_ratio_d, txt.stock_ratio)
    unique_stock_refs_card = card_styling(unique_stock_refs_d, txt.number_of_sku)
    unique_sales_refs_card = card_styling(unique_sales_refs_d, txt.unique_prod_sold)
    stockout_ref_count_card = card_styling(stockout_ref_count_d, "Stockout Risk Count")

    return current_stocks_card, period_sales_card, stock_ratio_card, unique_stock_refs_card, unique_sales_refs_card, stockout_ref_count_card


# download button
download_button = html.Button('Button 1', id='btn-nclicks-1', n_clicks=0),


# SIDEBAR
# sidebar = html.Div(
#     [
#         html.H3(txt.inventory_tracker, style={'color': styles.main_blue, 'text-align': 'center'}),
#         html.Hr(style={'border-top': '5px solid ' + styles.light_grey}),
#         dbc.Nav(
#             [
#                 dbc.NavLink(txt.overview_txt, href="/overview"),
#                 dbc.NavLink(txt.supplier_level, href="/suppliers", active=True),
#             ],
#             vertical=True,
#         ),
#     ],
#     style=styles.SIDEBAR_STYLE,
# )

# NAVBAR
navbar = dbc.NavbarSimple(
    children=[
        dbc.Nav(
            [
                dbc.NavLink(txt.overview_txt, href="/overview"),
                dbc.NavLink(txt.supplier_level, href="/suppliers"),
            ],
        ),
    ],

    brand=txt.inventory_tracker,
    brand_href="/suppliers",
    style=styles.NAVBAR_STYLE,
    color=styles.main_blue,
    dark=True,
)
