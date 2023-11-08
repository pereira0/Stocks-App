# app.py
import dash
import pandas as pd
from dash import Output, Input, dcc, html, ctx
import dash_bootstrap_components as dbc
import webbrowser
import openpyxl
# import json
from json import loads
# get other local files
import assets.styles
import data_cleanup
import tables
import variables
import components
import supplier_stock_tracker
import overview_page

# initialize dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])

# setup layout for app
app.layout = html.Div([
    dcc.Location(id="url"),
    # components.sidebar,
    components.navbar,
    dbc.Container(id='page-content', style=assets.styles.CONTENT_STYLE)

    ],
    style=assets.styles.PAGE_STYLE)

# Define the URL for your Dash app and open it automatically
url = 'http://127.0.0.1:8050/'
webbrowser.open_new(url)


# CALLBACKS
# NAVBAR CALLBACK
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/overview":
        return overview_page.content
    elif pathname == "/suppliers":
        return supplier_stock_tracker.content
    elif pathname == "/":
        return overview_page.content
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


# MAIN PAGE CALL BACK
@app.callback(
    Output("current_stocks_card", "children"),
    Output("period_sales_card", "children"),
    Output("stock_ratio_card", "children"),
    Output("unique_stock_refs_card", "children"),
    Output("unique_sales_refs_card", "children"),
    Output("stockout_ref_count_card", "children"),
    Output("main_stock_table", "children"),
    Output("session_storage", "data"),
    Output("table_without_stock", "children"),
    Input("dropdown-button", "value")
)
def update_name(supplier_name):
    sales_prediction, current_stocks, total_sales, stock_ratio, unique_sales_refs, \
        unique_stock_refs, stockout_ref_count, stocks_without_sales = \
        data_cleanup.cleanup_full_data(variables.sales_file, variables.start_date, variables.end_date,
                          supplier_name, variables.stock_file, variables.predict_month,
                          variables.date_start_txt, variables.date_format)

    current_stocks_card, period_sales_card, stock_ratio_card, unique_stock_refs_card, \
        unique_sales_refs_card, stockout_ref_count_card = \
        components.create_display_cards(current_stocks, total_sales, stock_ratio,
                                        unique_stock_refs, unique_sales_refs,
                                        stockout_ref_count)

    table_stock = tables.get_main_stock_table(sales_prediction)
    table_stock_out = tables.stock_without_sales_table(stocks_without_sales)
    df_as_json = sales_prediction.to_json()

    return current_stocks_card, period_sales_card, stock_ratio_card,unique_stock_refs_card, \
           unique_sales_refs_card, stockout_ref_count_card, table_stock, df_as_json, table_stock_out


# DOWNLOAD BUTTON CALLBACK
# inputs: the actual button and a component where data was stored as a json from the main page callback
# outputs: no visual outputs, it downloads an excel
@app.callback(
    Output('download-dataframe-xlsx', 'data'),
    Input('btn-download-txt', 'n_clicks'),
    Input('session_storage', 'data'),
)
def download_data(n_clicks, value_json):
    if "btn-download-txt" == ctx.triggered_id:
        # fetch data from json storage, transpose and reset index
        data_df = pd.DataFrame.from_dict(loads(value_json), orient="index")
        data_df = data_df.transpose()
        data_df = data_df.reset_index(drop=True)
        return dcc.send_data_frame(data_df.to_excel, "mydf.xlsx")


if __name__ == '__main__':
    app.run_server(debug=False)
