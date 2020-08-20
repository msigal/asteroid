import json


def mock_data(filename):
    with open(filename, 'r', encoding='utf8') as file:
        data = file.read()
    return json.loads(data).get('near_earth_objects')
