import json
import unicodedata


def json_(path, data=None):
    if data is None:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    validate = json.dumps(data)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def normalize(char):
    return unicodedata.normalize('NFKD', char).encode('ascii', 'ignore').decode('ascii')


def normalize_name(name: str):
    return ''.join([normalize(x) for x in name if x.isalpha()]).lower()
