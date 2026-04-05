import pandas as pd

file_path = "data/financial_data.csv" 

df = pd.read_csv(file_path)
pd.set_option('display.max_rows', None)


print(df)