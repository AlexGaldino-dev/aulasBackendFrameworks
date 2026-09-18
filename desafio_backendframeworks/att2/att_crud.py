"""
Lab 2 - Desafio: Mini API de Tarefas com CRUD completo

Veja o enunciado completo em lab2/desafio/enunciado.md

Como executar:
    python lab2/desafio/todo_app_crud_esqueleto.py
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

tarefas = [
    {"id": 1, "titulo": "Estudar Flask", "concluida": False},
    {"id": 2, "titulo": "Revisar o desafio anterior", "concluida": True},
    {"id": 3, "titulo": "Esturar Java e Spring", "concluida": False}
]
proximo_id = 4

@app.route('/')
def index():
    return jsonify({
        "mensagem": "Bem-vindo à Mini API de Tarefas!",
        "rotas_disponiveis": {
            "listar_tarefas": "/tarefas",
            "tarefa_por_id": "/tarefas/<id>",
            "tarefas_pendentes": "/tarefas/pendentes",
            "sobre": "/sobre"
        }
    })

@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    return jsonify(tarefas), 200


@app.route('/tarefas/<int:id>', methods=['GET'])
def buscar_tarefa(id):
    tarefa = next((t for t in tarefas if t["id"] == id), None)
    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    return jsonify(tarefa), 200


@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    global proximo_id

    # Content-Type precisa ser application/json
    if not request.is_json:
        return jsonify({"erro": "Content-Type deve ser application/json"}), 415

    # silent=True evita erro 400 automático do Flask se o JSON for inválido
    dados = request.get_json(silent=True)

    # "titulo" é obrigatório (e não pode ser vazio)
    if not isinstance(dados, dict) or not str(dados.get("titulo", "")).strip():
        return jsonify({"erro": "O campo 'titulo' é obrigatório"}), 400

    nova_tarefa = {
        "id": proximo_id,
        "titulo": dados["titulo"],
        "concluida": bool(dados.get("concluida", False)),
    }
    tarefas.append(nova_tarefa)
    proximo_id += 1

    return jsonify(nova_tarefa), 201


@app.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    tarefa = next((t for t in tarefas if t["id"] == id), None)
    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    if not request.is_json:
        return jsonify({"erro": "Content-Type deve ser application/json"}), 415

    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({"erro": "Corpo JSON inválido"}), 400

    # Só atualiza campos permitidos (o "id" nunca é alterado)
    if "titulo" in dados:
        if not str(dados["titulo"]).strip():
            return jsonify({"erro": "O campo 'titulo' não pode ser vazio"}), 400
        tarefa["titulo"] = dados["titulo"]
    if "concluida" in dados:
        tarefa["concluida"] = bool(dados["concluida"])

    return jsonify(tarefa), 200


@app.route('/tarefas/<int:id>', methods=['DELETE'])
def remover_tarefa(id):
    global tarefas

    tarefa = next((t for t in tarefas if t["id"] == id), None)
    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    tarefas = [t for t in tarefas if t["id"] != id]

    return "", 204


if __name__ == '__main__':
    app.run(debug=True)
