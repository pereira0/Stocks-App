# IMPORTS
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import variables

# DATA
sales_file = variables.sales_file
stock_file = variables.stock_file

# LOCAL VARIABLES
predict_month = variables.predict_month
start_date = date.today().replace(day=1) - relativedelta(years=1)
end_date = start_date + relativedelta(months=predict_month + 1) - relativedelta(days=1)
date_start_txt = start_date.strftime('%Y-%m')
date_end_txt = end_date.strftime('%Y-%m')


# FUNCTIONS
# cleanup sales data
def cleanup_sales_data(sales_file_d, start_date_d, end_date_d):
    # change type of date column
    sales_file_d['datatempo'] = pd.to_datetime(sales_file_d['datatempo']).dt.date

    # mark with an 'e' the sales for last year's month that occurred before the same day as today
    sales_file_d['dateF'] = sales_file_d.apply(lambda x: x['datatempo'].strftime('%Y-%m')
    if x['datatempo'] > (date.today() - relativedelta(years=1))
    else (x['datatempo'].strftime('%Y-%m') + 'e'), axis=1)
    # filter data for appropriate months
    sales_file_d = sales_file_d[(sales_file_d['datatempo'] >= date.today().replace(day=1))
                                | ((sales_file_d['datatempo'] >= start_date_d) & (
            sales_file_d['datatempo'] <= end_date_d))]

    # drop unnecessary columns
    sales_file_d = sales_file_d.drop(['datatempo', 'ano', 'mes'], axis=1)

    # create pivot table
    sales_data = sales_file_d.pivot_table(index=['ref', 'design'], columns='dateF', values='qtt',
                                          aggfunc='sum').reset_index().rename_axis(None, axis=1)

    # turn NaN to 0
    sales_data.loc[:, :] = sales_data.loc[:, :].fillna(0)

    # calculate time period sales
    name_of_col = 'sales_' + str(predict_month) + '_months'

    # sum all columns except the current months sales
    sales_data[name_of_col] = sales_data[
        [col for col in sales_data.columns if (col.startswith('202') and col != date.today().strftime('%Y-%m'))]].sum(
        axis=1)

    # reorder columns
    cols = sales_data.columns.tolist()
    sales_data = sales_data[cols]

    return sales_data, name_of_col


# merge stocks with sales
def merge_stocks_sales(sales_data, stocks_file, name_of_col):
    stocks_file = stocks_file[['ref', 'design', 'stock']]

    # join sales table with stocks
    sales_data['ref'] = sales_data['ref'].apply(lambda x: x.strip())
    stocks_file['ref'] = stocks_file['ref'].apply(lambda x: x.strip())
    final_df = pd.merge(sales_data, stocks_file, on='ref', how='right')

    # drop useless columns
    final_df = final_df.drop(['design_y'], axis=1)

    # fill NA
    final_df.loc[:, :] = final_df.loc[:, :].fillna(0)

    # calculate sales / stock ratio
    final_df['ratio'] = (final_df['stock'] / final_df[name_of_col]).round(2)

    # fill NA
    final_df.loc[:, :] = final_df.loc[:, :].fillna(0)

    return final_df

# create predictions
def sales_predictions(final_df_d, date_start_txt, predict_month_d):
    # create prediction for end of current month
    try:
        final_df_d[(date.today().strftime('%Y-%m') + 'e')] = final_df_d[date.today().strftime('%Y-%m')] + final_df_d[
            date_start_txt]
    except:
        try:
            final_df_d[(date.today().strftime('%Y-%m') + 'e')] = final_df_d[date.today().strftime('%Y-%m')]
        except:
            final_df_d[(date.today().strftime('%Y-%m') + 'e')] = final_df_d[date_start_txt]

    # drop current sales of this month
    try:
        final_df = final_df_d.drop([date.today().strftime('%Y-%m')], axis=1)
    except:
        print("no df")

    # correct first month
    try:
        final_df[date_start_txt] = final_df[date_start_txt] + final_df[(date_start_txt + 'e')]
        # drop remaining of the first month
        final_df = final_df.drop([(date_start_txt + 'e')], axis=1)

    except:
        final_df = final_df.rename(columns={(date_start_txt + 'e'): date_start_txt})

    # start creating stock prediction
    final_df[(date.today().strftime('%Y-%m') + 'e')] = final_df['stock'] - final_df[(date.today().strftime('%Y-%m') + 'e')]

    # create month variables
    date_month_pred = date.today().replace(day=1) + relativedelta(months=1)

    # create prediction months for stocks
    for i in range(1, predict_month_d):
        date_pred = date_month_pred + relativedelta(months=i - 1)
        date_previous = date_month_pred + relativedelta(months=i - 2)
        month_corresp = date_month_pred + relativedelta(months=i - 13)
        col_name = (date_pred.strftime('%Y-%m') + 'e')
        col_name_anterior = (date_previous.strftime('%Y-%m') + 'e')
        col_name_mes_corresp = month_corresp.strftime('%Y-%m')

        final_df[col_name] = final_df[col_name_anterior] - final_df[col_name_mes_corresp]

    final_df.sort_values(by=['ref'])

    return final_df


# RUN CODE
sales_data, name_of_col = cleanup_sales_data(sales_file, start_date, end_date)
merged_stocks_sales = merge_stocks_sales(sales_data, stock_file, name_of_col)
sales_prediction = sales_predictions(merged_stocks_sales, date_start_txt, predict_month)

