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
    def __init__(self, start_date, end_date, api_key):
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.api_key = api_key

    def get_data_bw_two_dates(self):
        current_date = self.start_date
        all_data = pd.DataFrame()

        while current_date <= self.end_date:
            next_date = current_date + timedelta(days=100 - 1)  # Subtract 1 day to avoid overlapping dates
            next_date = min(next_date, self.end_date)  # Make sure we don't go beyond the end_date

            p_vehicle = GetDataFromAPI(current_date.strftime("%Y-%m-%d"), next_date.strftime("%Y-%m-%d"), self.api_key)
            data_vehicle_hourly = p_vehicle.get_data_from_open_data_paris()

            all_data = pd.concat([all_data, data_vehicle_hourly], ignore_index=True)

            # Move to the next date range
            current_date = next_date + timedelta(days=1)

        return all_data

if __name__ == '__main__':
    PATH = Path('data/')
    print("creating directory structure...")
    PATH.mkdir(exist_ok=True)

    api_key = ''
    start_date = '2021-05-17'
    end_date = '2023-06-10'

    p_data = DataBetweenDates(start_date, end_date, api_key)
    data = p_data.get_data_bw_two_dates()

    # Now 'data' contains all the data between the specified start and end dates.
    # You can save it to parquet or CSV as needed.
    data.to_parquet(PATH / 'all_vehicle_data.parquet')
    data.to_csv(PATH / 'all_vehicle_data.csv')