# app.py
import dash
import dash_core_components as dcc
import dash_html_components as html
import webbrowser
# get other local files
import data_cleanup

# get data
sales_prediction = data_cleanup.sales_prediction

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Stock Tracker"),
    dash.dash_table.DataTable(sales_prediction.to_dict('records'), [{"name": i, "id": i} for i in sales_prediction.columns]),
    dcc.Graph(id='example-graph',
              figure={
                  'data': [
                      {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Trace 1'},
                      {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Trace 2'},
                  ],
                  'layout': {
                      'title': 'Sample Bar Chart'
                  }
              })
])

# Define the URL for your Dash app
url = 'http://127.0.0.1:8050/'

# Automatically open the web browser to the specified URL
webbrowser.open_new(url)

if __name__ == '__main__':
    app.run_server(debug=False)
