#!/usr/bin/env python3

from flask import Flask
from flask_restful import reqparse, abort, Resource, Api

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("task")

TODOs = {
    1: {"task": "build an API"},
    2: {"task": "????"},
    3: {"task": "profit!"}
}

def abort_if_todo_not_found(todo_id):
    if todo_id not in TODOs:
        abort(404, message="TODO {} does not exist".format(todo_id))


def add_todo(todo_id):
    args = parser.parse_args()
    todo = {"task": args["task"]}
    TODOs[todo_id] = todo
    return todo

class Todo(Resource):
    """Show a single TODO item, allow deletions, modifications
    """
    def get(self, todo_id):
        # reads (cRud)
        abort_if_todo_not_found(todo_id)
        return TODOs[todo_id]

    def delete(self, todo_id):
        # deletions (cruD)
        abort_if_todo_not_found(todo_id)
        del TODOs[todo_id]
        return "", 204
    
    def put(self, todo_id):
        # updates (crUd)
        return add_todo(todo_id), 201

class TodoList(Resource):
    """Show all TODOs and allow creating new TODO objects
    """
    def get(self):
        # read all (cRud)
        return TODOs
    
    def post(self):
        # create (Crud)
        todo_id = max(TODOs.keys()) + 1
        return add_todo(todo_id), 201

api.add_resource(Todo, "/todos/<int:todo_id>")
api.add_resource(TodoList, "/todos")

if __name__ == "__main__":
    app.run(debug=True)
