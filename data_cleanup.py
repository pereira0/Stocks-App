# IMPORTS
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import variables

# DATA
sales_file = variables.sales_file
stock_file = variables.stock_file

# LOCAL VARIABLES
date_format = variables.date_format
predict_month = variables.predict_month
start_date = date.today() - relativedelta(years=1)
end_date = start_date + relativedelta(months=predict_month + 1) - relativedelta(days=1)
date_start_txt = start_date.strftime(date_format)
date_end_txt = end_date.strftime(date_format)


# FUNCTIONS
# cleanup sales data
def cleanup_sales_data(sales_file_d, start_date_d, end_date_d, predict_month):
    # change type of date column
    sales_file_d['datatempo'] = pd.to_datetime(sales_file_d['datatempo']).dt.date

    # filter data for past year
    sales_file_d = sales_file_d[(sales_file_d['datatempo'] >= start_date_d) & (sales_file_d['datatempo'] <= end_date_d)]

    # create marker for year and month only
    sales_file_d['dateF'] = sales_file_d.apply(lambda x: x['datatempo'].strftime(date_format), axis=1)

    # total sales
    sales_file_d['total'] = sales_file_d['qtt'] * sales_file_d['unit_price']

    return sales_file_d


# prep cleaned sales data for main table
def prep_data_for_main_table(sales_file_d, predict_month):
    # only carry necessary cols
    sales_file_d = sales_file_d[['dateF', 'ref', 'design', 'qtt']]

    # create pivot table
    sales_data = sales_file_d.pivot_table(index=['ref', 'design'], columns='dateF', values='qtt',
                                          aggfunc='sum').reset_index().rename_axis(None, axis=1)

    # turn NaN to 0
    sales_data.loc[:, :] = sales_data.loc[:, :].fillna(0)

    # calculate time period sales
    name_of_col_f = 'sales_' + str(predict_month) + '_months'

    # sum all columns except the current months sales
    sales_data[name_of_col_f] = sales_data[[col for col in sales_data.columns if (col.startswith('2'))]].sum(axis=1)

    return sales_data, name_of_col_f


# merge stocks with sales
def merge_stocks_sales(sales_data_d, stocks_file, name_of_col_d):
    stocks_file = stocks_file[['ref', 'design', 'stock']]

    # join sales table with stocks
    sales_data_d['ref'] = sales_data_d['ref'].apply(lambda x: x.strip())
    stocks_file['ref'] = stocks_file['ref'].apply(lambda x: x.strip())
    final_df = pd.merge(sales_data_d, stocks_file, on='ref', how='right')

    # drop useless columns
    final_df = final_df.drop(['design_x'], axis=1)

    # fill NA
    final_df.loc[:, :] = final_df.loc[:, :].fillna(0)

    # filter to products that had sales
    final_df = final_df[(final_df['sales_12_months'] > 0)]

    # calculate sales / stock ratio
    final_df['ratio'] = (final_df['stock'] / final_df[name_of_col_d]).round(2)

    return final_df


# create predictions
def sales_predictions(final_df_d, date_start_txt_d, predict_month_d):
    # create prediction for end of current month
    try:
        final_df_d[(date.today().strftime(date_format) + 'e')] = final_df_d[date.today().strftime(date_format)] + \
                                                                 final_df_d[
                                                                     date_start_txt_d]
    except:
        try:
            final_df_d[(date.today().strftime(date_format) + 'e')] = final_df_d[date.today().strftime(date_format)]
        except:
            final_df_d[(date.today().strftime(date_format) + 'e')] = final_df_d[date_start_txt_d]

    # drop current sales of this month
    try:
        final_df_d = final_df_d.drop([date.today().strftime(date_format)], axis=1)
    except:
        print("no df")

    # correct first month
    try:
        final_df_d[date_start_txt_d] = final_df_d[date_start_txt_d] + final_df_d[(date_start_txt_d + 'e')]
        # drop remaining of the first month
        final_df_d = final_df_d.drop([(date_start_txt_d + 'e')], axis=1)

    except:
        final_df_d = final_df_d.rename(columns={(date_start_txt_d + 'e'): date_start_txt_d})

    # start creating stock prediction
    final_df_d[(date.today().strftime(date_format) + 'e')] = final_df_d['stock'] - final_df_d[
        (date.today().strftime(date_format) + 'e')]

    # create month variables
    date_month_pred = date.today().replace(day=1) + relativedelta(months=1)

    # create prediction months for stocks
    for i in range(1, predict_month_d):
        date_pred = date_month_pred + relativedelta(months=i - 1)
        date_previous = date_month_pred + relativedelta(months=i - 2)
        month_corresp = date_month_pred + relativedelta(months=i - 13)
        col_name = (date_pred.strftime(date_format) + 'e')
        col_name_anterior = (date_previous.strftime(date_format) + 'e')
        col_name_mes_corresp = month_corresp.strftime(date_format)

        final_df_d[col_name] = final_df_d[col_name_anterior] - final_df_d[col_name_mes_corresp]

    final_df_d = final_df_d.sort_values(by=['ref'])

    # move column 'design' and 'ref' to the beginning
    final_df_d = final_df_d[['design_y'] + [col for col in final_df_d.columns if col != 'design_y']]
    final_df_d = final_df_d[['ref'] + [col for col in final_df_d.columns if col != 'ref']]

    # create list of dates on the table
    col_list = []
    for col in final_df_d.columns:
        if ("2" in col) & ("e" not in col):
            col_list.append(col)

    # Drop historical sales months
    final_df_d = final_df_d.drop(col_list, axis=1)

    # rename columns
    final_df_d = final_df_d.rename(columns={"design_y": "name", "sales_12_months": "sales", "ref": "code"})

    return final_df_d


# get main indicators
def main_indicators(stock_file_d, clean_sales_df, display_df_d):
    # get total stocks
    stock_file_d['total'] = stock_file_d['stock'] * stock_file_d['unit_price']
    current_stocks_d = stock_file_d['total'].sum()
    current_stocks_string = "{:,.0f}€".format(current_stocks_d).replace(',', '.')

    # get sales for the period
    total_sales_d = clean_sales_df['total'].sum()
    total_sales_string = "{:,.0f}€".format(total_sales_d).replace(',', '.')

    # ratio
    stock_ratio_d = current_stocks_d / total_sales_d
    stock_ratio_string = "{:.2f}".format(stock_ratio_d)

    # total number of codes sold in period
    unique_sales_refs_d = clean_sales_df['ref'].nunique()

    # total number of codes in inventory
    unique_stock_refs_d = stock_file_d['ref'].nunique()

    # refs that will go out of stock in the time period
    stockout_ref_count_d = sum(display_df_d.ratio < 1)

    return current_stocks_string, total_sales_string, stock_ratio_string, \
           unique_sales_refs_d, unique_stock_refs_d, stockout_ref_count_d


# get a df with the products that didn't get any sales
def get_stocks_without_sales(sales_data_d, stock_file_d):
    stock_file_d = stock_file_d[['ref', 'design', 'stock']]

    # join sales table with stocks
    sales_data_d['ref'] = sales_data_d['ref'].apply(lambda x: x.strip())
    stock_file_d['ref'] = stock_file_d['ref'].apply(lambda x: x.strip())
    final_df_d = pd.merge(sales_data_d, stock_file_d, on='ref', how='right')
    # get only nan
    final_df_d = final_df_d[final_df_d['design_x'].isna()]
    # get only specific columns
    final_df_d = final_df_d[['ref', 'design_y', 'stock']]
    # get only stock bigger than 0
    final_df_d = final_df_d[(final_df_d['stock'] > 0)]
    # rename columns
    final_df_d = final_df_d.rename(columns={"design_y": "name", "ref": "code"})

    return final_df_d


# get a list of all suppliers
def get_list_of_suppliers(stock_file_d):
    list_of_suppliers_d = stock_file_d['suppliers'].unique()
    return list_of_suppliers_d.tolist()


# RUN CODE
sales_file_cleaned = cleanup_sales_data(sales_file, start_date, end_date, predict_month)
sales_data, name_of_col = prep_data_for_main_table(sales_file_cleaned, predict_month)
merged_stocks_sales = merge_stocks_sales(sales_data, stock_file, name_of_col)
sales_prediction = sales_predictions(merged_stocks_sales, date_start_txt, predict_month)
current_stocks, total_sales, stock_ratio, unique_sales_refs, unique_stock_refs, stockout_ref_count = main_indicators(
    stock_file, sales_file_cleaned, sales_prediction)
stocks_without_sales = get_stocks_without_sales(sales_data, stock_file)
list_of_suppliers = get_list_of_suppliers(stock_file)
