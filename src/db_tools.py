from utils import json_


def parse_form(form, keys):
    query = {key: form.get(key).strip()
             for key in keys if form.get(key, '').strip()
             }
    if 'id' in query:
        query['id'] = int(query['id'])
    return query


def get_valid_id(path):
    data = json_(path)
    ids = [x['id'] for x in data]
    ids.sort()
    return ids[-1] + 1
