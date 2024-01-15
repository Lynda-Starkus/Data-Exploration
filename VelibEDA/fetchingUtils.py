import pandas as pd
import numpy as np
import requests
import json
from pathlib import Path
from datetime import date, timedelta
import warnings
warnings.filterwarnings('ignore')




class GetDataFromAPI():

    def __init__(self, start_date, end_date, api_key):
        self.start_date = start_date
        self.end_date = end_date
        self.api_key = api_key


    def get_data_from_open_data_paris(self):
        '''
        https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?where=duedate%20%3E%20date%272023%27&limit=100
        '''

        #/api/records/1.0/search/?dataset=comptage-multimodal-comptages&q=t%3A%5B2021-10-10%20TO%202023-09-09%5D&rows=101
        url = 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?where=duedate%20%3E%20date%272018%27'.format(self.start_date,self.end_date)
        print(url)
        response = requests.get(url)
        print(response.status_code)
        data = json.loads(response.content)['records']
    

        records = []
        for record in data:
            records.append(record['fields'])

        df = pd.DataFrame(records)
        
        return df
    

if __name__ == '__main__':
    PATH = Path('data/')
    print("creating directory structure...")
    (PATH).mkdir(exist_ok=True)

    start_date = '2023-05-17'
    end_date = '2023-06-10'
    api_key = ''
    get_data_class = GetDataFromAPI(start_date, end_date, api_key)
    data = get_data_class.get_data_from_open_data_paris()
#    data['metric_and_value'] = data['metric_and_value'].astype(str)  ## error in saving to parquet version in the newer version so need to convert this column to str

    data_path = PATH/'vehichle_count_hourly_{}_to_{}.parquet'.format(start_date, end_date)
    data.to_parquet(data_path)