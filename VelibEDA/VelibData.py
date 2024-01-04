import yaml
import pandas as pd
from requests import make_request

class VelibData:

    def VelibData(self):
        self.station_info_url, self.station_status_url  = self.getStationUrl()

        # Requêtes API Velib
        stations_information_response = make_request(self.station_info_url)
        stations_status_response = make_request(self.station_status_url)
        self.stations_information = pd.DataFrame(stations_information_response.json()['data']['stations'])
        self.stations_status = pd.DataFrame(stations_status_response.json()['data']['stations'])



    def getStationUrl(self):
        import yaml
        yaml_file_path = './conf.yaml'

        with open(yaml_file_path, 'r') as file:
            config_data = yaml.safe_load(file)

        return config_data['api_url']['station_information'], config_data['api_url']['station_status']

    def getStationsInfo(self):
        return self.stations_information

    def getStationsStatus(self):
        return self.stations_status


if __name__ == "__main__":
    
    velibData = VelibData()
    stationsInfo = VelibData.getStationsInfo()
    stationsStatus = VelibData.getStationsStatus()

    print("Infos: \n", stationsInfo.head(10))
    print("Status: \n", stationsStatus.head(10))

