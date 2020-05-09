#Copyright (c) Microsoft Corporation. All rights reserved.
#Licensed under the MIT License. #Signed up for account so license and endpoint are unique 

# -*- coding: utf-8 -*-

import json
import os
from pprint import pprint
import requests

# Add your Bing Search V7 subscription key and endpoint to your environment variables.
subscription_key = os.environ['BING_KEY']
endpoint = 'https://watchmework.cognitiveservices.azure.com' + "/bing/v7.0/search"

#TODO: Resolve subscription key and endpoint issues

# Query term(s) to search for.
query = "Watch me Work"

# Construct a request
mkt = 'en-US'
params = { 'q': query, 'mkt': mkt }
headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

# Call the API
try:
    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()

    print("\nHeaders:\n")
    print(response.headers)

    print("\nJSON Response:\n")
    pprint(response.json())
except Exception as ex:
    raise ex
