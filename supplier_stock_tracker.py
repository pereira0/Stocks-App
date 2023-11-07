# IMPORTS
import dash
from dash import Output, Input, dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# get other local files
import assets.styles as styles
import data_cleanup
import tables
import variables
import components

# get dropdown
list_of_suppliers_loc = data_cleanup.get_list_of_suppliers(variables.stock_file)
dropdown_select = components.create_dropdown_supplier_selector(list_of_suppliers_loc)

content = dbc.Container([

        dbc.Row([
            dbc.Col(html.H3("SUPPLIER LEVEL", style={'color': styles.main_blue})),
            dbc.Col(dropdown_select)
        ]),


        dbc.Row([
            dbc.Col(id='current_stocks_card', style=styles.LEFT_CARD_STYLE),
            dbc.Col(id='period_sales_card'),
            dbc.Col(id='stock_ratio_card', style=styles.RIGHT_CARD_STYLE),
            # dbc.Col(id='unique_stock_refs_card'),
            # dbc.Col(id='unique_sales_refs_card'),
            # dbc.Col(id='stockout_ref_count_card')
        ],
            style=styles.ROW_CARD_STYLE

        ),

        dbc.Row([
            # dbc.Col(id='current_stocks_card'),
            # dbc.Col(id='period_sales_card'),
            # dbc.Col(id='stock_ratio_card'),
            dbc.Col(id='unique_stock_refs_card', style=styles.LEFT_CARD_STYLE),
            dbc.Col(id='unique_sales_refs_card'),
            dbc.Col(id='stockout_ref_count_card', style=styles.RIGHT_CARD_STYLE)
        ],
            style=styles.ROW_CARD_STYLE

        ),

        dbc.Row([
            dbc.Row(html.H6("Inventory Tracker")),
            dbc.Row(id='main_stock_table'),
        ],
            style=styles.CONTAINER_CARD),

        dbc.Row([
            dbc.Row(html.H6("Products in inventory without sales")),
            dbc.Row(id='table_without_stock'),
        ],
            style=styles.CONTAINER_CARD),

    ],

    style=styles.SPECIFIC_CONTENT_STYLE
)



