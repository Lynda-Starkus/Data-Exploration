import yaml

class VelibData:

    def VelibData(self):
        self.station_info_url, self.station_status_url  = self.getStationUrl()


    def getStationUrl():
        import yaml
        yaml_file_path = './conf.yaml'

        with open(yaml_file_path, 'r') as file:
            config_data = yaml.safe_load(file)

        return config_data['api_url']['station_information'], config_data['api_url']['station_status']


