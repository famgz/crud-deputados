import json


def json_(path, data=None):
    with open(path, encoding='utf-8') as f:
        if data is None:
            return json.load(f)
        json.dump(data)
