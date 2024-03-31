from flask import Flask, request
from utils import json_, get_last_id
from config import deputados_path, frentes_path

app = Flask('app')


deputados_query_keys = ['id', 'nome', 'siglaPartido', 'siglaUf']


@app.post('/deputados')
def create_deputado():
    return


@app.get('/deputados')
def get_deputados():
    form = request.form
    query = {key: form.get(key)
             for key in deputados_query_keys if form.get(key)
             }
    if query.get('id'):
        query['id'] = int(query['id'])
    deputados = json_(deputados_path)
    if not query:
        return deputados
    return [dep for dep in deputados if any(
        [True for k, v in query.items() if dep[k] == v])]


if __name__ == '__main__':
    app.run(debug=True)  # localhost:5000
