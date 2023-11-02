import pandas as pd

# FILE LOCATIONS
sales_file = pd.read_csv('data/sales_data_aaa.csv', delimiter=';')
stock_file = pd.read_csv('data/stock_data_aaa.csv', delimiter=';')

# VARIABLES
predict_month = 12

# FORMATS
date_format = '%y/%m'  # date formatting
