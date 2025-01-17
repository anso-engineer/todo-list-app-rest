from flask import request,jsonify
from models import Contexts, Spaces, Tasks
from datetime import datetime


def register_routes(app, db):

    @app.route('/')
    def home():
        return "Welcome home!"

    # CONTEXTS
    @app.route('/contexts')
    def get_contexts():
        result = Contexts.query.all() # return empty array
        output = [context.to_dict() for context in result]
        return jsonify(output), 200

    # SPACES
    @app.route('/spaces')
    def get_spaces():
        result = Spaces.query.all() # return empty array
        output = [space.to_dict() for space in result]
        return jsonify(output), 200

    @app.route('/spaces/<int:space_id>', methods=['DELETE'])
    def delete_space(space_id):
        space = Spaces.query.get(space_id)
        if not space:
            return jsonify({"error": "Space not found"}), 404

        try:
            db.session.delete(space)
            db.session.commit()
            return jsonify({"message": "Space deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    #TASKS
    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        result = Tasks.query.filter_by(Completed = False).all() # return empty array
        output = [task.to_dict() for task in result]
        return jsonify(output), 200

    @app.route('/tasks', methods=['POST'])
    def add_task():
        # Extract data from the request body
        data = request.get_json()

        # Validate required fields
        required_fields = ['name', 'description', 'postponed_status', 'priority',
                           'complexity', 'creation_date', 'completion_date',
                           'completed', 'is_template', 'repeated']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        # Create a new task instance
        new_task = Tasks(
            Name=data['name'],
            Description=data['description'],
            PostponedStatus=data['postponed_status'],
            Priority=data['priority'],
            Complexity=data['complexity'],
            CreationDate=data['creation_date'],
            CompletionDate=data['completion_date'],
            Completed=data['completed'],
            IsTemplate=data['is_template'],
            Repeated=data['repeated']
        )

        try:
            # Add to the database
            db.session.add(new_task)
            db.session.commit()

            # Return the created task as a response
            return jsonify(new_task.to_dict()), 201
        except Exception as e:
            # Handle potential errors
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    def edit_task(task_id):
        # Get the JSON data from the request
        data = request.get_json()

        # Find the task by ID
        task = Tasks.query.get(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        # Update task fields (only if provided in the request)
        if "name" in data:
            task.Name = data["name"]
        if "description" in data:
            task.Description = data["description"]
        if "postponed_status" in data:
            task.PostponedStatus = data["postponed_status"]
        if "priority" in data:
            task.Priority = data["priority"]
        if "complexity" in data:
            task.Complexity = data["complexity"]
        if "creation_date" in data:
            task.CreationDate = data["creation_date"]
        if "completion_date" in data:
            task.CompletionDate = data["completion_date"]
        if "completed" in data:
            task.Completed = data["completed"]
        if "is_template" in data:
            task.IsTemplate = data["is_template"]
        if "repeated" in data:
            task.Repeated = data["repeated"]

        try:
            # Commit changes to the database
            db.session.commit()
            return jsonify(task.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        # Find the task by ID
        task = Tasks.query.get(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        try:
            # Delete the task from the database
            db.session.delete(task)
            db.session.commit()
            return jsonify({"message": "Task deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


    #TEMPLATES
    @app.route('/templates', methods=['GET'])
    def get_templates():
        result = Tasks.query.filter_by(IsTemplate=True).all()
        output = [task.to_dict() for task in result]
        return jsonify(output), 200

    @app.route('/templates/open', methods=['GET'])
    def get_teplate_open():
        result = Tasks.query.filter(Tasks.IsTemplate == 1, Tasks.Completed == 1).all()
        output = [task.to_dict() for task in result]
        return jsonify(output), 200

    @app.route('/templates/active', methods=['GET'])
    def get_template_active():
        result = Tasks.query.filter(Tasks.IsTemplate == 1, Tasks.Completed == 0).all()
        output = [task.to_dict() for task in result]
        return jsonify(output), 200

    @app.route('/templates', methods=['POST'])
    def add_task_template():
        # Get the JSON data from the request
        data = request.get_json()

        # Find the task by ID
        task = Tasks.query.get(data["task_template_id"])
        if not task:
            return jsonify({"error": "Task not found"}), 404

        if "priority" in data:
            task.Priority = data["priority"]
        if "complexity" in data:
            task.Complexity = data["complexity"]

        if "mark_completed" in data: #close task
            task.Completed = 1
            task.CompletionDate = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        else:                        #reopen task
            task.Completed = 0
            task.CompletionDate = None
            task.Repeated = task.Repeated + 1
            task.CreationDate = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        try:
            db.session.commit()
            return jsonify(task.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500