from flask import Flask, request, jsonify
from models.task import Task
app = Flask(__name__)

tasks = []
task_id_control = 1

@app.route("/tasks", methods=["POST"])
def create_task():
  global task_id_control
  data = request.get_json()
  new_task = Task(id=task_id_control, title=data["title"], description=data.get("description", ""))
  task_id_control += 1
  tasks.append(new_task.to_dict())
  return jsonify({"message": "Nova tarefa criada com sucesso"}), 201

@app.route("/tasks", methods=["GET"])
def get_tasks():
  total_tasks = len(tasks)
  output = {
    "tasks": tasks,
    "total_tasks": total_tasks
  }
  return jsonify(output), 200

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
  task = next((task for task in tasks if task["id"] == task_id), None)
  if task:
    return jsonify(task), 200
  return jsonify({"message": "Tarefa não encontrada"}), 404

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
  data = request.get_json()
  task = next((task for task in tasks if task["id"] == task_id), None)
  if task:
    task.update(data)
    return jsonify({"message": "Tarefa atualizada com sucesso"}), 200
  return jsonify({"message": "Tarefa não encontrada"}), 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
  task = next((task for task in tasks if task["id"] == task_id), None)
  if task:
    tasks.remove(task)
    return jsonify({"message": "Tarefa deletada com sucesso"}), 200
  return jsonify({"message": "Tarefa não encontrada"}), 404

if __name__ == "__main__":
  app.run(debug=True)
