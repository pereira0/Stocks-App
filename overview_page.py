import dash_bootstrap_components as dbc
import assets
import historical_data as hd
from dash import Output, Input, dcc, html, ctx
import assets.styles as styles

figure_test = hd.figure_for_show


content = dbc.Container([

        dbc.Row(
            [dbc.Col(html.H1("Overview"))]
        ),

        
        dbc.Row(
            [dcc.Graph(id='december-chart', figure=figure_test)],
            style=styles.CONTAINER_CARD
        )],
        style=assets.styles.SPECIFIC_CONTENT_STYLE


)