import json


def get_last_id(path):
    data = json_(path)
    ids = [x['id'] for x in data]
    ids.sort()
    return ids[-1] + 1


def json_(path, data=None):
    with open(path, encoding='utf-8') as f:
        if data is None:
            return json.load(f)
        json.dump(data)
