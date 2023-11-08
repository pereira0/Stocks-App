import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import local_data

# # LOCAL FILE LOCATIONS
sales_file = pd.read_csv('data/sales_data_aaa.csv', delimiter=';')
stock_file = pd.read_csv('data/stock_data_aaa.csv', delimiter=';')

# DATABASE DATA
# sales_file = local_data.sales_data_from_db
# stock_file = local_data.stock_query_from_db

# FORMATS
date_format = '%y/%m'  # date formatting

# VARIABLES
predict_month = 12
start_date = date.today() - relativedelta(years=1)
end_date = start_date + relativedelta(months=predict_month + 1) - relativedelta(days=1)
date_start_txt = start_date.strftime(date_format)
date_end_txt = end_date.strftime(date_format)


