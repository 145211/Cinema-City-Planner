import os

import requests
import json
import Addresses


def download_json_file(url, destination, cinema):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            json_data = response.json()
            with open(destination, 'w', encoding='utf-8') as file:
                json.dump(json_data, file, ensure_ascii=False, indent=4)
            print("{} JSON file downloaded and saved successfully.".format(cinema))
        except json.JSONDecodeError:
            print("Failed to parse {} JSON file.".format(cinema))
    else:
        print("Failed to download {} file.".format(cinema))


addressesGit = Addresses.addressesGit

for x in addressesGit.keys():
    url = addressesGit[x]
    local_folder = os.path.dirname(os.path.abspath(__file__))
    destination = f'{local_folder}/screenings/{x}.json'
    download_json_file(url, destination, x)
