import os
import json
from flask import Flask, redirect, url_for, request, make_response
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
from Cache import Cache

cache = Cache(10)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)

load_dotenv()
client = MongoClient(
    os.environ['MONGODB_HOST'],
    # os.environ['MONGODB_HOST_SCRIPT'],
    int(os.environ['MONGODB_PORT']))

database = os.environ['MONGODB_DATABASE']
collection = os.environ['MONGODB_COLLECTION']

db = client[database]

@app.route('/')
def home():
    return 'Visite: https://documenter.getpostman.com/view/150117/SW7Ucqpi?version=latest'

"""
Rota para testar o funcionamento do cache
"""
@app.route('/cache')
def caching():
    for i in range(20):
      cache.set(i,i)
    results = JSONEncoder().encode(cache.dump())
    resp = make_response(results, 200)
    resp.mimetype = "application/json"
    return resp


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
        'data_inicio': {'$gte': arguments['data_inicio'], '$lte': arguments['data_fim']}
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
@app.route('/campus/<campus_name>/cursos')
def campus_cursos(campus_name):
    # db.students.aggregate([
    #     { $match: {'campus': "TL"}},
    # {"$group":{_id: {campus: "$campus", curso: "$curso"}}}
    #
    # ])
    pipeline = [
        {"$match": {'campus': campus_name}},
        {"$group": {"_id": {"campus": "$campus", "curso": "$curso"}}}
    ]
    _results = db[collection].aggregate(pipeline)
    items = [item for item in _results]
    results = JSONEncoder().encode(items)
    resp = make_response(results, 200)
    resp.mimetype = "application/json"
    return resp


"""
3. Descobrir número total de alunos num campus em um dado período
a. Tipo de requisição: [a definir]
b. Parâmetros: campus, data de início e data de fim
c. Retorno: número de alunos do campus no período
"""
@app.route('/campus/<campus_name>/total_alunos')
def alunos_campus(campus_name):
    arguments = request.args.to_dict()
    pipeline = [
        {"$match": {
            'campus': campus_name,
            'data_inicio': {
                '$gte': arguments['data_inicio'], 
                '$lte': arguments['data_fim']
                }
            },
        },
        {"$group": {"_id": campus_name, "count": {"$sum": 1}}}
    ]
    _results = db[collection].aggregate(pipeline)
    items = [item for item in _results]
    results = JSONEncoder().encode(items[0])
    resp = make_response(results, 200)
    resp.mimetype = "application/json"
    return resp


"""
4. Cadastrar alunos
a. Tipo da requisição: [a definir]
b. Parâmetros: nome, idade_ate_31_12_2016, ra, campus, município, curso, modalidade,
nivel_do_curso, data_inicio
c. Retorno: sucesso/erro
"""
@app.route('/alunos', methods=['POST'])
def aluno_create():
    aluno = {
        'nome': request.form['nome'],
        'idade_ate_31_12_2016': request.form['idade_ate_31_12_2016'],
        'ra': request.form['ra'],
        'campus': request.form['campus'],
        'municipio': request.form['municipio'],
        'curso': request.form['curso'],
        'modalidade': request.form['modalidade'],
        'nivel_do_curso': request.form['nivel_do_curso'],
        'data_inicio': request.form['data_inicio']
    }
    insert_result = db[collection].insert_one(aluno)
    if(insert_result.acknowledged):
        aluno["_id"] = insert_result.inserted_id
        #caching
        cache.set(aluno['ra'],aluno)
        return 'sucesso'
    else:
        return 'erro'

"""
5. Buscar aluno
a. Tipo da requisição: [a definir]
b. Parâmetro: ra
c. Retorno: todos os dados do aluno
"""
@app.route('/alunos/<ra>')
def aluno_get(ra):
    aluno = cache.get(ra)
    if not aluno:
        aluno = db[collection].find_one({'ra':ra})
        if aluno:
            cache.set(aluno['ra'],aluno)
        else:
            return make_response('', 404)

    results = JSONEncoder().encode(aluno)
    resp = make_response(results, 200)
    resp.mimetype = "application/json"
    return resp

"""
6. Remover aluno do banco
a. Tipo da requisição: [a definir]
b. Parâmetros: ra, campus
c. Retorno: sucesso/erro
"""
@app.route('/alunos/<ra>', methods=['DELETE'])
def aluno_delete(ra):
    result = db[collection].remove({'ra':ra})
    print()
    if result['ok'] and result['n'] > 0:
        cache.unset(ra)
        return "sucesso"
    return "erro"


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)