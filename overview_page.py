import dash_bootstrap_components as dbc
import dash_html_components as html
import assets

content = dbc.Container([

        dbc.Row(
            [dbc.Col(html.H1("Overview"))])],
        style=assets.styles.SPECIFIC_CONTENT_STYLE


)