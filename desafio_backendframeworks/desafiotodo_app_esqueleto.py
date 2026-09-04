"""
Bloco 3 - Desafio: Mini API de Tarefas (TodoList)

Veja o enunciado completo em desafio/enunciado.md

Como executar:
    python desafio/todo_app_esqueleto.py
"""
from flask import Flask, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False # corrigir o erro em que o Jason retorna '\u00e9' em letras com acento

tarefas = [
    {"id": 1, "titulo": "Estudar Flask", "concluida": False, "prioridade": "alta"},
    {"id": 2, "titulo": "Fazer exercícios de rotas", "concluida": False, "prioridade": "media"},
    {"id": 3, "titulo": "Revisar conceitos de JSON", "concluida": True, "prioridade": "baixa"},
    {"id": 4, "titulo": "Refazer tudo isso aqui em golang", "concluida": False, "prioridade": "baixa"},
    {"id": 5, "titulo": "Estudar java + Springbot", "concluida": False, "prioridade": "alta"}
]


# Rota Raiz com algumas informações simples de como acessar as tarefas
@app.route('/')
def index():
    return jsonify({
        "mensagem": "Bem-vindo a sua Lista de tarefas",
        "rotas_disponiveis": {
            "listar_tarefas": "/tarefas",
            "tarefa_por_id": "/tarefas/id",
            "tarefas_pendentes": "/tarefas/pendentes",
            "sobre": "/sobre"
        }
    })


# Retorna todas as tarefas em JSON
@app.route('/tarefas')
def listar_tarefas():
    return jsonify(tarefas)


# Retorna apenas as tarefas que ainda NÃO foram concluidas
@app.route('/tarefas/pendentes')
def listar_tarefas_pendentes():
    pendentes = [tarefa for tarefa in tarefas if not tarefa["concluida"]]
    return jsonify(pendentes)


# Busca a tarefa pelo id.
# Se não encontrar, retorna jsonify com erro e status 404.
@app.route('/tarefas/<int:id>')
def buscar_tarefa(id):
    for tarefa in tarefas:
        if tarefa["id"] == id:
            return jsonify(tarefa)
    return jsonify({"erro": f"Tarefa com id {id} não encontrada."}), 404


# Retorna um JSON com dados da equipe/aluno (nome, turma, etc)
@app.route('/sobre')
def sobre():
    return jsonify({
        "nome": "Alex Gadino",
        "turma": "4º período Noite",
        "projeto": "Mini API de Tarefas (TodoList)",
        "bloco": "Bloco 3"
    })


if __name__ == '__main__':
    app.run(debug=True)
