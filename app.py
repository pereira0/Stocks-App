# app.py
import dash
from dash import Output, Input
import dash_html_components as html
import dash_bootstrap_components as dbc
import webbrowser
# get other local files
import data_cleanup
import tables
import variables
# import navbar
import components


# get dropdown
list_of_suppliers_loc = data_cleanup.get_list_of_suppliers(variables.stock_file)
dropdown_select = components.create_dropdown_supplier_selector(list_of_suppliers_loc)


# initialize dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])

# setup layout for app
app.layout = dbc.Container(
    [
        # navbar unecessary at this point
        # navbar.navbar,

        dbc.Row(
            [dbc.Col(html.H1("Stock Tracker")),
             dbc.Col(dropdown_select)]),

        dbc.Row([
            dbc.Col(id='current_stocks_card'),
            # dbc.Col(period_sales_card),
            # dbc.Col(stock_ratio_card)
        ]),

        # dbc.Row([
        #     dbc.Col(unique_stock_refs_card),
        #     dbc.Col(unique_sales_refs_card),
        #     dbc.Col(stockout_ref_count_card)
        # ]),

        dbc.Row([dbc.Col(html.H2("Selected Supplier", id="selected-supplier"))]),

        dbc.Row([dbc.Col(html.H2("Inventory Tracker"))]),

        # dbc.Row(dbc.Col(tables.get_main_stock_table(sales_prediction))),

        dbc.Row([dbc.Col(html.H2("Products in inventory without sales"))]),

        # dbc.Row(dbc.Col(tables.stock_without_sales_table(stocks_without_sales))),


    ],
    style={'padding': '1rem'}
)


# Define the URL for your Dash app
url = 'http://127.0.0.1:8050/'

# Automatically open the web browser to the specified URL
webbrowser.open_new(url)


# CALLBACKS
@app.callback(
    Output("selected-supplier", "children"),
    Output("current_stocks_card", "children"),
    Input("dropdown-button", "value")
)
def update_name(supplier_name):
    print(supplier_name)
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

    return supplier_name, current_stocks_card


if __name__ == '__main__':
    app.run_server(debug=False)
