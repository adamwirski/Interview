# importing the requests library
import json

import requests

def get_data(lat, lng, date):
    # api-endpoint
    URL = "https://api.sunrisesunset.io/json"

    # location given here
    location = "delhi technological university"

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'lat': lat, 'lng': lng, 'timezone': 'UTC', 'date': date}

    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)
    text = json.loads(r.text)
    return text['results']
    # extracting data in json format
    # data = r.json()