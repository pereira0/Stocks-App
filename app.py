# app.py
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import webbrowser
# get other local files
import data_cleanup
import tables
# import navbar
import components

# get data
sales_prediction = data_cleanup.sales_prediction
current_stocks_card, period_sales_card, stock_ratio_card = components.create_display_cards(data_cleanup.current_stocks,
                                                                                           data_cleanup.total_sales,
                                                                                           data_cleanup.stock_ratio)



# initialize dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])

# setup layout for app
app.layout = dbc.Container(
    [
        # navbar unecessary at this point
        # navbar.navbar,

        dbc.Row(
            [dbc.Col(html.H1("Stock Tracker")),
             dbc.Col(components.dropdown)]),

        dbc.Row([
            dbc.Col(current_stocks_card),
            dbc.Col(period_sales_card),
            dbc.Col(stock_ratio_card)
        ]),

        dbc.Row(dbc.Col(tables.get_main_stock_table(sales_prediction))),
    ],
    style={'padding': '1rem'}
)

# Define the URL for your Dash app
url = 'http://127.0.0.1:8050/'

# Automatically open the web browser to the specified URL
webbrowser.open_new(url)

if __name__ == '__main__':
    app.run_server(debug=False)
