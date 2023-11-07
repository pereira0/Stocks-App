import dash
import assets.styles as st


# conditional formatting for main data
def style_data_conditional_formatting(sales_prediction):
    # conditional formatting for main table that is the same for every selection
    formatting_list = [
        {'if': {'column_id': 'ratio'}, 'backgroundColor': st.light_blue, 'color': st.proj_white},
        {'if': {'column_id': 'sales'}, 'backgroundColor': st.light_blue, 'color': st.proj_white},
        {'if': {'column_id': 'stock'}, 'backgroundColor': st.light_blue, 'color': st.proj_white},
        {'if': {'filter_query': '{ratio} <= 1', 'column_id': 'ratio'}, 'backgroundColor': st.purple, 'color': st.proj_white},
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


# main table with stock predictions
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
        # filter_action='native',  # create filters
        fixed_rows={'headers': True},
        style_table={
            'overflowX': 'auto',
            'height': '500px',
            'overflowY': 'auto',
            'fontSize': 15},
        style_header={
            'backgroundColor': 'transparent',
            'color': st.main_blue
        },
        style_data={
            'backgroundColor': 'transparent',
            'color': st.main_blue
        },
        style_data_conditional=style_data_conditional_list,
        style_header_conditional=[
            {'if': {'column_id': 'name'}, 'textAlign': 'left'},
            {'if': {'column_id': 'code'}, 'textAlign': 'center'}],
        page_action='none',
    )

    return table


# create table for stocks without sales
def stock_without_sales_table(stocks_without_sales_d):
    table = dash.dash_table.DataTable(
            data=stocks_without_sales_d.to_dict('records'),
            columns=[{"name": i, "id": i} for i in stocks_without_sales_d.columns],
            merge_duplicate_headers=True,  # remove duplicates from top row
            style_header={
                'backgroundColor': 'transparent',
                'color': st.proj_white
            },
            style_data={
                'backgroundColor': 'transparent',
                'color': st.light_grey
            },
            fixed_rows={'headers': True},
            style_table={'overflowX': 'auto', 'height': '500px', 'overflowY': 'auto', 'fontSize': 15},
            style_header_conditional=[
                {'if': {'column_id': 'name'}, 'textAlign': 'left'},
                {'if': {'column_id': 'code'}, 'textAlign': 'center'}],
            style_data_conditional=[
                {'if': {'column_id': 'name'}, 'textAlign': 'left'},
                {'if': {'column_id': 'code'}, 'textAlign': 'center'}],
            page_action='none',
            fill_width=False
        )

    return table

