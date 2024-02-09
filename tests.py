import pytest
import requests

# CRUD
BASE_URL= 'http://127.0.0.1:5000'
tasks = []

def test_create_task():
  new_task_data = {
    "title": "Nova tarefa",
    "description": "Descrição da nova tarefa"
  }
  response = requests.post(f'{BASE_URL}/tasks', json=new_task_data)
  assert response.status_code == 201
  response_json = response.json()
  assert response_json["message"] == "Nova tarefa criada com sucesso"
  assert "id" in response_json
  tasks.append(response_json["id"])

def test_get_tasks():
  response = requests.get(f'{BASE_URL}/tasks')
  assert response.status_code == 200
  response_json = response.json()
  assert "tasks" in response_json
  assert "total_tasks" in response_json

def test_get_task():
  if tasks:
    response = requests.get(f'{BASE_URL}/tasks/{tasks[0]}')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == tasks[0]

def test_update_task():
  if tasks:
    payload = {
      "title": "Tarefa atualizada",
      "description": "Descrição da tarefa atualizada",
      "completed": True,
    }
    response = requests.put(f'{BASE_URL}/tasks/{tasks[0]}', json=payload)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["message"] == "Tarefa atualizada com sucesso"

    # Nova requisição a tarefa específica
    response = requests.get(f'{BASE_URL}/tasks/{tasks[0]}')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["title"] == payload["title"]
    assert response_json["description"] == payload["description"]
    assert response_json["completed"] == payload["completed"]

def test_delete_task():
  if tasks:
    response = requests.delete(f'{BASE_URL}/tasks/{tasks[0]}')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["message"] == "Tarefa deletada com sucesso"

    # Nova requisição a tarefa específica
    response = requests.get(f'{BASE_URL}/tasks/{tasks[0]}')
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["message"] == "Tarefa não encontrada"

    # Remover da lista de tarefas
    tasks.pop(0)