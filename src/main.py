from flask import Flask, request
from utils import json_, get_valid_id, parse_form
from config import deputados_path, frentes_path

app = Flask('app')

deputados_read_keys = ['id', 'nome', 'siglaPartido', 'siglaUf']
deputados_create_keys = ['nome', 'siglaPartido', 'siglaUf']


@app.post('/deputados')
def create_deputado():

    return


@app.get('/deputados')
def get_deputados():
    form = request.form
    query = parse_form(form, deputados_read_keys)
    deputados = json_(deputados_path)
    if not query:
        return deputados
    return [dep for dep in deputados if any(
        [True for k, v in query.items() if dep[k] == v])]


if __name__ == '__main__':
    app.run(debug=True)  # localhost:5000
