import dash

def get_main_stock_table(sales_prediction):
    table = dash.dash_table.DataTable(
                data=sales_prediction.to_dict('records'),
                columns=[{"name": i, "id": i} for i in sales_prediction.columns],
                style_table={'overflowX': 'auto'},
                style_data_conditional=[
                        {
                            'if': {
                                'filter_query': '{ratio} <= 1',
                                'column_id': 'ratio'
                            },
                            'backgroundColor': 'tomato',
                            'color': 'white'
                        },
                        {
                            'if': {'column_id': 'name'},
                            'textAlign': 'left'
                        },
                        {
                            'if': {'column_id': 'code'},
                            'textAlign': 'center'
                        },

                ],
                style_header_conditional=[
                            {
                                'if': {'column_id': 'name'},
                                'textAlign': 'left'
                            },
                            {
                            'if': {'column_id': 'code'},
                            'textAlign': 'center'
                            },
                        ]
            )

    return table