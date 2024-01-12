import pandas as pd 

df = pd.read_parquet('data/vehicles_preprocessed/[Paris] Amsterdam x Clichy.parquet', engine='fastparquet')

print(df)