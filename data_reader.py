import json


def read_json_data(filename):
    with open(filename) as file:
        return json.load(file)
