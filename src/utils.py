import json


def parse_form(form, keys):
    query = {key: form.get(key)
             for key in keys if form.get(key)
             }
    if 'id' in query:
        query['id'] = int(query['id'])
    return query


def get_valid_id(path):
    data = json_(path)
    ids = [x['id'] for x in data]
    ids.sort()
    return ids[-1] + 1


def json_(path, data=None):
    with open(path, encoding='utf-8') as f:
        if data is None:
            return json.load(f)
        json.dump(data)
