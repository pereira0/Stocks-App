# IMPORTS
import dash
from dash import Output, Input, dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# get other local files
import assets.styles
import data_cleanup
import tables
import variables
import components

# get dropdown
list_of_suppliers_loc = data_cleanup.get_list_of_suppliers(variables.stock_file)
dropdown_select = components.create_dropdown_supplier_selector(list_of_suppliers_loc)

content = dbc.Container([

        dbc.Row([dbc.Col(dropdown_select)]),

        dbc.Row([
            dbc.Col(id='current_stocks_card'),
            dbc.Col(id='period_sales_card'),
            dbc.Col(id='stock_ratio_card')
            ],
            style=assets.styles.ROW_CARD_STYLE

        ),

        dbc.Row([
            dbc.Col(id='unique_stock_refs_card'),
            dbc.Col(id='unique_sales_refs_card'),
            dbc.Col(id='stockout_ref_count_card')
            ],
            style=assets.styles.ROW_CARD_STYLE
        ),

        dbc.Row([dbc.Col(html.H2("Inventory Tracker"))]),

        dbc.Row(dbc.Col(id='main_stock_table')),

        # dbc.Row(dbc.Col(id='download_button')),

        dbc.Row([dbc.Col(html.H2("Products in inventory without sales"))]),

        dbc.Row(dbc.Col(id='table_without_stock')),


    ],

    style=assets.styles.SPECIFIC_CONTENT_STYLE
)



