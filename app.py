from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo-list-app.db'
    db.init_app(app)

    from routes import register_routes
    register_routes(app, db)

    migrate = Migrate(app, db)

    # Enable CORS for origins matching http://localhost:517*
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": r"http://localhost:517\d+"}})

    return app

