import csv
import schedule
import time
import yaml
import pandas as pd
import requests

class VelibData:
    def __init__(self):
        self.station_info_url, self.station_status_url = self.getStationUrl()

        # Requêtes API Velib
        stations_information_response = make_request(self.station_info_url)
        stations_status_response = make_request(self.station_status_url)
        self.stations_information = pd.DataFrame(stations_information_response.json()['data']['stations'])
        self.stations_status = pd.DataFrame(stations_status_response.json()['data']['stations'])

    def getStationUrl(self):
        yaml_file_path = './conf.yaml'
        with open(yaml_file_path, 'r') as file:
            config_data = yaml.safe_load(file)
        return config_data['api_url']['station_information'], config_data['api_url']['station_status']

    def getStationsInfo(self):
        return self.stations_information

    def getStationsStatus(self):
        return self.stations_status

def make_request(path: str):
    return requests.get(path)

def save_to_csv(data, csv_filename):
    try:
        with open(csv_filename, 'r') as f:
            pass  # File exists
    except FileNotFoundError:
        with open(csv_filename, 'w', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(data.columns)

    with open(csv_filename, 'a', newline='') as f:
        data.to_csv(f, index=False, header=False)

def job():
    velibData = VelibData()
    stationsInfo = velibData.getStationsInfo()
    stationsStatus = velibData.getStationsStatus()

    # Combine the information and status data (modify as needed)
    combined_data = pd.concat([stationsInfo, stationsStatus], axis=1)

    # Save the combined data to a CSV file
    save_to_csv(combined_data, "output.csv")

if __name__ == "__main__":
    # Schedule the job to run every 1 minute
    schedule.every(1).minutes.do(job)

    # Infinite loop to keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for 1 second to avoid high CPU usage
