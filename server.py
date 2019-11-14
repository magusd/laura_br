import os
import json
from flask import Flask, redirect, url_for, request, make_response
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)

load_dotenv()
client = MongoClient(
    os.environ['MONGODB_HOST'],
    int(os.environ['MONGODB_PORT']))

database = os.environ['MONGODB_DATABASE']
collection = os.environ['MONGODB_COLLECTION']

db = client[database]

@app.route('/')
def home():
    return db[collection].find_one({})

@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'name': request.form['name'],
        'description': request.form['description']
    }
    db.tododb.insert_one(item_doc)

    return redirect(url_for('todo'))


"""
1. Listar todos os itens de uma modalidade em um período ordenados por data
a. Tipo da requisição: GET
b. Parâmetros: modalidade, data de início e data de fim
c. Retorno: lista de todos os itens com modalidade, filtrando pelo período
passado e ordenando de forma decrescente pela data dos
documentos.
"""
@app.route('/alunos/modalidades')
def alunos_modalidades():
    arguments = request.args.to_dict()
    query = {
        'modalidade': arguments['tipo'],
        'data_inicio': {'$gte': arguments['data_inicio'], '$lt': arguments['data_fim']}
    }
    _results = db[collection].find(query)
    items = [item for item in _results]
    results = JSONEncoder().encode(items)
    resp = make_response(results, 200)
    resp.mimetype = "application/json"
    return resp



"""
2. Listar todos os cursos de um campus
a. Tipo da requisição: [a definir]
b. Parâmetros: campus
c. Retorno: lista de cursos do campus
"""


"""
3. Descobrir número total de alunos num campus em um dado período
a. Tipo de requisição: [a definir]
b. Parâmetros: campus, data de início e data de fim
c. Retorno: número de alunos do campus no período
"""
"""
4. Cadastrar alunos
a. Tipo da requisição: [a definir]
b. Parâmetros: nome, idade_ate_31_12_2016, ra, campus, município, curso, modalidade,
nivel_do_curso, data_inicio
c. Retorno: sucesso/erro
"""
"""
5. Buscar aluno
a. Tipo da requisição: [a definir]
b. Parâmetro: ra
c. Retorno: todos os dados do aluno
"""
"""
6. Remover aluno do banco
a. Tipo da requisição: [a definir]
b. Parâmetros: ra, campus
c. Retorno: sucesso/erro
"""



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)