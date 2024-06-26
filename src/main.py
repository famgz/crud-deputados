from flask import Flask, request
from utils import json_, normalize_name
from db_tools import get_valid_id, parse_form
from config import deputados_path, frentes_path
import traceback

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


@app.route('/deputados', methods=['POST', 'GET', 'DELETE'])
def deputados():
    try:
        form = request.form
        match request.method:
            case 'POST':
                return write('deputados', form)
            case 'GET':
                return read('deputados', form)
            case 'DELETE':
                return delete_by_id('deputados', form)
            case _:
                return 'Invalid method'
    except Exception as e:
        print(traceback.format_exc())
        return f'ERRO: {e}'


@app.route('/frentes', methods=['POST', 'GET', 'DELETE'])
def frentes():
    try:
        form = request.form
        match request.method:
            case 'POST':
                return write('frentes', form)
            case 'GET':
                return read('frentes', form)
            case 'DELETE':
                return delete_by_id('frentes', form)
            case _:
                return 'Invalid method'
    except Exception as e:
        print(traceback.format_exc())
        return f'ERRO: {e}'


def write(type_, form):
    path = KEYS[type_]['path']
    query_keys = KEYS[type_]['write']
    parsed_form = parse_form(form, query_keys)
    missing_keys = [key for key in query_keys if key not in parsed_form]
    if missing_keys:
        raise Exception(
            f'Modo de escrita com parâmetros inválidos ou ausentes: {", ".join(missing_keys)}')
    id_ = get_valid_id(path)
    items = json_(path)
    match type_:
        case 'deputados':
            nome = parsed_form['nome']
            nome_exists = [True for x in items if x['nome'] == nome]
            if nome_exists:
                raise Exception(
                    f'O nome do deputado \"{nome}\" já está cadastrado')
            new_entry = {
                'id': id_,
                'uri': f'https://dadosabertos.camara.leg.br/api/v2/deputados/{id_}',
                'nome': nome,
                'siglaPartido': parsed_form['siglaPartido'].upper(),
                'uriPartido': 'https://dadosabertos.camara.leg.br/api/v2/partidos/0000',
                'siglaUf': parsed_form['siglaUf'][:2].upper(),
                'idLegislatura': 57,
                'urlFoto': f'https://www.camara.leg.br/internet/deputado/bandep/{id_}.jpg',
                'email': f'dep.{normalize_name(nome)}.leg.br',
                'id_frente': 000,
            }
        case 'frentes':
            titulo = parsed_form['titulo']
            titulo_exists = [True
                             for x in items if x['titulo'] == titulo]
            if titulo_exists:
                raise Exception(
                    f'O título \"{titulo}\" já está cadastrado')
            new_entry = {
                'id': id_,
                'uri': f'https://dadosabertos.camara.leg.br/api/v2/frentes/{id_}',
                'titulo': titulo,
                'idLegislatura': 57
            }
        case _:
            raise Exception(f'Tipo de database inválido: {type_}')
    items.append(new_entry)
    json_(path, items)
    return new_entry


def read(type_, form):
    path = KEYS[type_]['path']
    items = json_(path)
    # return all items
    if not form:
        return items
    query_keys = KEYS[type_]['read']
    query = parse_form(form, query_keys)
    # search with not enough parameters
    if not query:
        raise Exception(
            f'Modo de leitura com parâmetros inválidos. Informe um ou mais dos seguintes parâmetros: \"{", ".join(query_keys)}\"')
    # search by ID
    if 'id' in query:
        id_ = query['id']
        item = [x for x in items if x['id'] == id_]
        if not item:
            return f'Item com ID \"{id_}\" não encontrado'
        return item[0]
    # search by parameters
    return [item for item in items if all(
        [True if item[k] == v else False for k, v in query.items()])]


def delete_by_id(type_, form):
    path = KEYS[type_]['path']
    items = json_(path)
    if 'id' not in form:
        raise Exception('É preciso informar um ID válido para deletar')
    id_ = int(form['id'])
    items_ids = [x['id'] for x in items]
    if id_ not in items_ids:
        raise Exception(f'ID {id_} não encontrado')
    items = [x for x in items if x['id'] != id_]
    json_(path, items)
    return f'Item com ID \"{id_}\" removido com sucesso de {type_}'


if __name__ == '__main__':
    app.run(debug=True)  # localhost:5000
