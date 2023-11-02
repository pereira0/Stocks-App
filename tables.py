import dash


def style_data_conditional_formatting(sales_prediction):
    formatting_list = [{
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
        }]

    # create list of dates on the table
    col_list = []
    for col in sales_prediction.columns:
        if ("2" in col):
            formatting_list.append({
                'if': {
                    'filter_query': "{" + col + '} <= 1',
                    'column_id': col
                },
                'backgroundColor': '#E8E8E8'
            })

    return formatting_list




def get_main_stock_table(sales_prediction):
    style_data_conditional_list = style_data_conditional_formatting(sales_prediction)

    table = dash.dash_table.DataTable(
                data=sales_prediction.to_dict('records'),
                columns=[{"name": i, "id": i} for i in sales_prediction.columns],
                style_table={'overflowX': 'auto'},
                style_data_conditional=style_data_conditional_list,

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