from flask import jsonify
from models import Contexts, Spaces, Tasks


def register_routes(app, db):

    @app.route('/')
    def home():
        return "Welcome home!"

    @app.route('/contexts')
    def get_contexts():
        result = Contexts.query.all() # return empty array
        output = [context.to_dict() for context in result]
        return jsonify(output), 200

    @app.route('/spaces')
    def get_spaces():
        result = Spaces.query.all() # return empty array
        output = [space.to_dict() for space in result]
        return jsonify(output), 200

    @app.route('/tasks')
    def get_tasks():
        result = Tasks.query.all() # return empty array
        output = [task.to_dict() for task in result]
        return jsonify(output), 200