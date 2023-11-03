import dash


def style_data_conditional_formatting(sales_prediction):
    # conditional formatting for main table that is the same for every selection
    formatting_list = [
        {'if': {'column_id': 'ratio'}, 'backgroundColor': '#FFFFDD'},
        {'if': {'column_id': 'sales'}, 'backgroundColor': '#FFFFDD'},
        {'if': {'column_id': 'stock'}, 'backgroundColor': '#FFFFDD'},
        {'if': {'filter_query': '{ratio} <= 1', 'column_id': 'ratio'}, 'backgroundColor': 'tomato', 'color': 'white'},
        {'if': {'column_id': 'name'}, 'textAlign': 'left'}, {'if': {'column_id': 'code'}, 'textAlign': 'center'},
        {'if': {'column_id': 'name'}, 'width': '10%'},
    ]

    # create list of dates on the table
    for col in sales_prediction.columns:
        if "2" in col:
            formatting_list.append({
                'if': {
                    'filter_query': "{" + col + '} <= 1',
                    'column_id': col
                },
                'backgroundColor': '#E8E8E8'
            })

    return formatting_list


def get_main_stock_table(sales_prediction):
    # fetch conditional data from another function
    style_data_conditional_list = style_data_conditional_formatting(sales_prediction)

    # cleanup headers and create multi headers list
    columns_list = []
    for col in sales_prediction.columns:
        if "2" in col:
            columns_list.append({"name": ['20' + col[:2], col[-3:-1]], "id": col})
        else:
            columns_list.append({"name": ['', col], "id": col})

    table = dash.dash_table.DataTable(
        data=sales_prediction.to_dict('records'),
        columns=columns_list,
        merge_duplicate_headers=True,  # remove duplicates from top row
        filter_action='native',  # create filters
        fixed_rows={'headers': True},
        style_table={'overflowX': 'auto', 'height': '500px', 'overflowY': 'auto', 'fontSize': 15},
        style_data_conditional=style_data_conditional_list,
        style_header_conditional=[
            {'if': {'column_id': 'name'}, 'textAlign': 'left'},
            {'if': {'column_id': 'code'}, 'textAlign': 'center'}],
        page_action='none',
        export_format='xlsx'
    )

    return table
