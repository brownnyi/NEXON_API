import requests
import numpy as np
import random
import time

headers = {
    "x-nxopen-api-key": "YOUR_API_KEY"
}

import requests
import time

headers = {
    "x-nxopen-api-key": "test_02285515ad15d7a8f3e36ed0365e7dd96ff4a0cf26fb8f03b434fdc59e131d4eefe8d04e6d233bd35cf2fabdeb93fb0d"
}

def get_all_names(headers, today):
    page = 1
    all_names = []

    while True:
        params = {"date": today, "page": page, "world_type": 0}
        response = requests.get("https://open.api.nexon.com/maplestory/v1/ranking/union", headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}")
        
        data = response.json()
        ranking_list = data.get("ranking", [])

        if not ranking_list:
            break

        for entry in ranking_list:
            all_names.append(entry["character_name"])
        
        page += 1
        time.sleep(1)  # To prevent 'Too Many Requests' errors

    return all_names


def get_ocid(headers, nameList):
    ocid = []
    for name in nameList:
        urlString = "https://open.api.nexon.com/maplestory/v1/id?character_name=" + name
        response = requests.get(urlString, headers = headers)
        ocid.append(response.json()['ocid'])
        time.sleep(1)
    return ocid

def user(headers, ocid):
    cnt = 0
    for o in ocid:
        urlString = "https://open.api.nexon.com/maplestory/v1/character/basic?ocid=" + o
        response = requests.get(urlString, headers = headers)
        if response.json()['access_flag'] == 'true':
            cnt += 1
    return cnt
  
