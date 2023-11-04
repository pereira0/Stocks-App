# IMPORTS
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta


# FUNCTIONS
# cleanup sales data and FILTER SUPPLIER
def cleanup_sales_stock_data(sales_file_d, start_date_d, end_date_d, supplier_d, stocks_file, date_format_d):
    # change type of date column
    sales_file_d['datatempo'] = pd.to_datetime(sales_file_d['datatempo']).dt.date

    # supplier filtering
    sales_file_d = sales_file_d[(sales_file_d['supplier'] == supplier_d)]

    # filter data for past year
    sales_file_d = sales_file_d[(sales_file_d['datatempo'] >= start_date_d) & (sales_file_d['datatempo'] <= end_date_d)]

    # create marker for year and month only
    sales_file_d['dateF'] = sales_file_d.apply(lambda x: x['datatempo'].strftime(date_format_d), axis=1)

    # total sales
    sales_file_d['total'] = sales_file_d['qtt'] * sales_file_d['unit_price']

    # supplier filtering on stocks
    stock_file_d = stocks_file[(stocks_file['suppliers'] == supplier_d)]

    # cleanup stock data
    stock_file_d = stock_file_d[['ref', 'design', 'stock', 'unit_price']]

    return sales_file_d, stock_file_d


# prep cleaned sales data for main table
def prep_data_for_main_table(sales_file_d, predict_month_d):
    # only carry necessary cols
    sales_file_d = sales_file_d[['dateF', 'ref', 'design', 'qtt']]

    # create pivot table
    sales_data_d = sales_file_d.pivot_table(index=['ref', 'design'], columns='dateF', values='qtt',
                                            aggfunc='sum').reset_index().rename_axis(None, axis=1)

    # turn NaN to 0
    sales_data_d.loc[:, :] = sales_data_d.loc[:, :].fillna(0)

    # calculate time period sales
    name_of_col_f = 'sales_' + str(predict_month_d) + '_months'

    # sum all columns except the current months sales
    sales_data_d[name_of_col_f] = sales_data_d[[col for col in sales_data_d.columns
                                                if (col.startswith('2'))]].sum(axis=1)

    return sales_data_d, name_of_col_f


# merge stocks with sales
def merge_stocks_sales(sales_data_d, stock_clean_d, name_of_col_d, start_date_d, date_format_d):
    # join sales table with stocks
    sales_data_d['ref'] = sales_data_d['ref'].apply(lambda x: x.strip())
    stock_clean_d['ref'] = stock_clean_d['ref'].apply(lambda x: x.strip())
    merged_stocks_sales_d = pd.merge(sales_data_d, stock_clean_d, on='ref', how='right')

    # drop useless columns
    merged_stocks_sales_d = merged_stocks_sales_d.drop(['design_x'], axis=1)

    # fill NA
    merged_stocks_sales_d.loc[:, :] = merged_stocks_sales_d.loc[:, :].fillna(0)

    # filter to products that had sales
    merged_stocks_sales_d = merged_stocks_sales_d[(merged_stocks_sales_d['sales_12_months'] > 0)]

    # calculate sales / stock ratio
    merged_stocks_sales_d['ratio'] = (merged_stocks_sales_d['stock'] / merged_stocks_sales_d[name_of_col_d]).round(2)

    # correct for months without sales for selected supplier
    names = merged_stocks_sales_d.columns
    first_col = start_date_d.strftime(date_format_d)
    col_check = [first_col]
    value = ''

    for i in range(1, 12):
        year = int(col_check[i - 1][:2])
        month = int(col_check[i - 1][-2:])
        if month == 12:
            value = str(year + 1) + '/01'
        elif 1 <= month < 9:
            value = str(year) + '/0' + str(month + 1)
        else:
            value = str(year) + '/' + str(month + 1)
        col_check.append(value)

    cycle = 0
    for i in col_check:
        if i not in names:
            merged_stocks_sales_d[i] = 0

    return merged_stocks_sales_d

# create predictions
def sales_predictions(final_df_d, date_start_txt_d, predict_month_d, date_format_d):
    # create prediction for end of current month
    try:
        final_df_d[(date.today().strftime(date_format_d) + 'e')] = final_df_d[date.today().strftime(date_format_d)] + \
                                                                 final_df_d[
                                                                     date_start_txt_d]
    except:
        try:
            final_df_d[(date.today().strftime(date_format_d) + 'e')] = final_df_d[date.today().strftime(date_format_d)]
        except:
            final_df_d[(date.today().strftime(date_format_d) + 'e')] = final_df_d[date_start_txt_d]

    # drop current sales of this month
    try:
        final_df_d = final_df_d.drop([date.today().strftime(date_format_d)], axis=1)
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
    final_df_d[(date.today().strftime(date_format_d) + 'e')] = final_df_d['stock'] - final_df_d[
        (date.today().strftime(date_format_d) + 'e')]

    # create month variables
    date_month_pred = date.today().replace(day=1) + relativedelta(months=1)

    # create prediction months for stocks
    for i in range(1, predict_month_d):
        date_pred = date_month_pred + relativedelta(months=i - 1)
        date_previous = date_month_pred + relativedelta(months=i - 2)
        month_corresp = date_month_pred + relativedelta(months=i - 13)
        col_name = (date_pred.strftime(date_format_d) + 'e')
        col_name_anterior = (date_previous.strftime(date_format_d) + 'e')
        col_name_mes_corresp = month_corresp.strftime(date_format_d)

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


# run all cleanup code and return final data
def cleanup_full_data(sales_file_d, start_date_d, end_date_d, supplier_d, stock_file_d, predict_month_d,
                      date_start_txt_d, date_format_d):
    sales_file_cleaned, stock_file_cleaned = cleanup_sales_stock_data(sales_file_d, start_date_d, end_date_d,
                                                                      supplier_d, stock_file_d, date_format_d)
    sales_data, name_of_col = prep_data_for_main_table(sales_file_cleaned, predict_month_d)
    merged_stocks_sales = merge_stocks_sales(sales_data, stock_file_cleaned, name_of_col, start_date_d, date_format_d)
    sales_prediction = sales_predictions(merged_stocks_sales, date_start_txt_d, predict_month_d, date_format_d)
    current_stocks, total_sales, stock_ratio, unique_sales_refs, unique_stock_refs, \
        stockout_ref_count = main_indicators(stock_file_cleaned, sales_file_cleaned, sales_prediction)
    stocks_without_sales = get_stocks_without_sales(sales_data, stock_file_cleaned)

    return sales_prediction, current_stocks, total_sales, stock_ratio, unique_sales_refs, \
           unique_stock_refs, stockout_ref_count, stocks_without_sales




