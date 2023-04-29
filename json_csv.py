import csv
import datetime
import os
import json


# class containing all matches scraped by country, which are in data directory
class JsonToCsv:
    def __init__(self, country):
        self.country = country
        # Get the list of all files and directories
        self.path = f'data/{self.country}'
        self.dir_list = os.listdir(self.path)
        self.json_list = []
        self.data_list = []
        self.file_name = f'{self.country}_{datetime.date.today()}.csv'
        # fields of data that are creating
        self.fields = ["match_id",
                       "country",
                       "league",
                       "referee",
                       "date",
                       "host",
                       "guest",
                       "host_goals",
                       "guest_goals",
                       "host_corners",
                       "guest_corners",
                       "host_shots",
                       "guest_shots",
                       "host_shots_on_target",
                       "guest_shots_on_target",
                       "host_shots_off_target",
                       "guest_shots_off_target",
                       "host_shots_woodwork",
                       "guest_shots_woodwork",
                       "host_shots_blocked",
                       "guest_shots_blocked",
                       "host_fouls",
                       "guest_fouls",
                       "host_yellow_cards",
                       "guest_yellow_cards",
                       "host_red_cards",
                       "guest_red_cards"]
        self.get_dir_list()

    # function which oens all files and add them to Jjson_list and transfe it to data_list
    def get_dir_list(self):
        for i in range(0, len(self.dir_list)):
            with open(f'{self.path}/{self.dir_list[i]}') as file:
                self.json_list.append(file.read())
                if json.loads(self.json_list[i])["country"]==self.country:
                    self.data_list.append(json.loads(self.json_list[i]))
                print(json.loads(self.json_list[i]))
        # creating host and guest goals out of result and removing result
        for match in self.data_list:
            result = match["result"]
            match["host_goals"] = result.split(" : ")[0]
            match["guest_goals"] = result.split(" : ")[1]
            match.pop("result")

    # print(data_list)
    def save_data_file(self):
        with open(self.path+"/"+self.file_name, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(self.data_list)

# print(datetime.date.today())
