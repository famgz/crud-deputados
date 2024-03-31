from flask import Flask, request
from utils import json_, get_valid_id, parse_form
from config import deputados_path, frentes_path

app = Flask('app')


keys = {
    'deputados': {
        'path': deputados_path,
        'read': ['id', 'nome', 'siglaPartido', 'siglaUf'],
        'write': ['nome', 'siglaPartido', 'siglaUf']
    },
    'frentes': {
        'path': frentes_path,
        'read': [],
        'write': []
    },
}


@app.post('/deputados')
def create_deputado():
    return write('deputados', request.form)


@app.get('/deputados')
def get_deputados():
    return read('deputados', request.form)


def write(type_):
    return


def read(type_):
    form = request.form
    query = parse_form(form, keys[type_]['read'])
    path = keys[type_]['path']
    items = json_(path)
    if not query:
        return items
    return [item for item in items if any(
        [True for k, v in query.items() if item[k] == v])]


if __name__ == '__main__':
    app.run(debug=True)  # localhost:5000
