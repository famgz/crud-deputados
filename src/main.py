from flask import Flask, request
from utils import json_, get_valid_id, parse_form
from config import deputados_path, frentes_path

app = Flask('app')

KEYS = {
    'deputados': {
        'path': deputados_path,
        'read': ['id', 'nome', 'siglaPartido', 'siglaUf'],
        'write': ['nome', 'siglaPartido', 'siglaUf']
    },
    'frentes': {
        'path': frentes_path,
        'read': ['id', 'titulo'],
        'write': ['titulo']
    },
}


@app.post('/deputados')
def create_deputado():
    try:
        return write('deputados', request.form)
    except Exception as e:
        return f'ERRO: {e}'


@app.get('/deputados')
def get_deputados():
    try:
        return read('deputados', request.form)
    except Exception as e:
        print(e)
        return f'ERRO: {e}'


@app.post('/frentes')
def create_frente():
    try:
        return write('frentes', request.form)
    except Exception as e:
        return f'ERRO: {e}'


@app.get('/frentes')
def get_frentes():
    try:
        return read('frentes', request.form)
    except Exception as e:
        return f'ERRO: {e}'


def write(type_, form):
    path = KEYS[type_]['path']
    query_keys = KEYS[type_]['write']
    query = parse_form(form, query_keys)
    missing_keys = [key for key in query_keys if key not in query]
    if missing_keys:
        raise Exception(
            f'Modo de escrita com parâmetros inválidos ou ausentes: {", ".join(missing_keys)}')
    items = json_(path)
    return 'ok'


def read(type_, form):
    path = KEYS[type_]['path']
    items = json_(path)
    # return all items
    if not form:
        return items
    query_keys = KEYS[type_]['read']
    query = parse_form(form, query_keys)
    # query search with not enough parameters
    if not query:
        raise Exception(
            f'Modo de leitura com parâmetros inválidos.<br>Informe um ou mais dos parâmetros: \"{", ".join(query_keys)}\"')
    # query by ID
    if 'id' in query:
        id_ = query['id']
        item = [x for x in items if x['id'] == id_]
        if not item:
            return f'Item com ID \"{id_}\" não encontrado'
        return item[0]
    # query by parameters
    return [item for item in items if any(
        [True for k, v in query.items() if item[k] == v])]


def update(type_, form):
    return


def delete(type_, form):
    return


if __name__ == '__main__':
    app.run(debug=True)  # localhost:5000
