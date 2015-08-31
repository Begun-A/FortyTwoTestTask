import os
import json


initial_data = os.path.join(os.path.dirname(__file__), 'initial_data.json')
with open(initial_data) as json_settings:
    settings = json.load(json_settings)
