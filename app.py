# app.py
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import webbrowser
# get other local files
import data_cleanup
import tables

# get data
sales_prediction = data_cleanup.sales_prediction

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])

app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H1("Stock Tracker"))),
        dbc.Row(dbc.Col(tables.get_main_stock_table(sales_prediction))),
    ]
)

# Define the URL for your Dash app
url = 'http://127.0.0.1:8050/'

# Automatically open the web browser to the specified URL
webbrowser.open_new(url)

if __name__ == '__main__':
    app.run_server(debug=False)
