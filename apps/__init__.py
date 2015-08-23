import os
import json


with open(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'hello/fixtures/initial_data.json'
    )
) as test_data:
    initial_data = json.load(test_data)


TEST_DATA = initial_data[0]['fields']
