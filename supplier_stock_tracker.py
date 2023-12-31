# IMPORTS
import dash_html_components as html
from dash import dcc
import dash_bootstrap_components as dbc
# get other local files
import assets.styles as styles
import data_cleanup
import variables
import components
import assets.text_translations as txt

# get dropdown
list_of_suppliers_loc = data_cleanup.get_list_of_suppliers(variables.stock_file)
dropdown_select = components.create_dropdown_supplier_selector(list_of_suppliers_loc)

content = dbc.Container([

        dbc.Row([
            dbc.Col(html.H3(txt.supplier_level, style={'color': styles.main_blue})),
            dbc.Col(dropdown_select)
        ]),


        dbc.Row([
            dbc.Col(id='current_stocks_card', style=styles.LEFT_CARD_STYLE),
            dbc.Col(id='period_sales_card'),
            dbc.Col(id='stock_ratio_card', style=styles.RIGHT_CARD_STYLE),
        ],
            style=styles.ROW_CARD_STYLE

        ),

        dbc.Row([
            dbc.Col(id='unique_stock_refs_card', style=styles.LEFT_CARD_STYLE),
            dbc.Col(id='unique_sales_refs_card'),
            dbc.Col(id='stockout_ref_count_card', style=styles.RIGHT_CARD_STYLE)
        ],
            style=styles.ROW_CARD_STYLE

        ),

        dbc.Row([
            dbc.Row(html.H6(txt.stocks_with_sales)),
            dbc.Row(id='main_stock_table'),
            dbc.Row([
                # DOWNLOAD BUTTON AND OTHER COMPONENTS
                dcc.Store(id='session_storage', storage_type='session'),  # component to store the data
                dbc.Button("Download excel", id="btn-download-txt", color="secondary", className="w-25 me-1"),  # physical view of the button
                dcc.Download(id="download-dataframe-xlsx")  # component to go on callback
            ], className='justify-content-end')

        ],
            style=styles.CONTAINER_CARD),

        dbc.Row([
            dbc.Row(html.H6(txt.inventory_no_sales)),
            dbc.Row(id='table_without_stock'),
        ],
            style=styles.CONTAINER_CARD),

    ],

    style=styles.SPECIFIC_CONTENT_STYLE
)



