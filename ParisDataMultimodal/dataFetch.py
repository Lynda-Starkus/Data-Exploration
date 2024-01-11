import pandas as pd
import numpy as np
import requests
import time
import os
from datetime import date, timedelta
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

from fetchingUtils import GetDataFromAPI

class DataBetweenDates:

    def __init__(self, start_date, end_date, api_key) -> list:
        self.start_date = start_date
        self.end_date = end_date
        self.api_key = api_key


    def get_data_bw_two_dates(self):


        path = '/data/vehicle_count_hourly_{}_to_{}.parquet'.format(self.start_date, self.end_date)
        path_csv = '/data/vehicle_count_hourly_{}_to_{}.csv'.format(self.start_date, self.end_date)

        if not os.path.exists(path) and not os.path.exists(path_csv):


            p_vehicle = GetDataFromAPI(start_date, end_date, api_key)


            data_vehicle_hourly = p_vehicle.get_data_from_open_data_paris()


#            PATH = Path('data/')


            data_vehicle_hourly_path = PATH/'vehicle_count_hourly_{}_to_{}.parquet'.format(self.start_date, self.end_date)
            data_vehicle_hourly.to_parquet(data_vehicle_hourly_path)

            data_vehicle_hourly_path_csv = PATH/'vehicle_count_hourly_{}_to_{}.csv'.format(self.start_date, self.end_date)
            data_vehicle_hourly.to_csv(data_vehicle_hourly_path_csv)

if __name__ == '__main__':
    PATH = Path('/data/')
    print("creating directory structure...")
    (PATH).mkdir(exist_ok=True)




    api_key = 'QRhUgmdXxbYTV8KMhgc2IYaKVUpVtJ9lqo2VKWvv'

    #today_date = date.today()
    #today_date = today_date.strftime("%Y-%m-%d")

    start_date = '2020-01-01'
    end_date =  '2023-05-01'

    p_data = DataBetweenDates(start_date, end_date, api_key)
    data = p_data.get_data_bw_two_dates()