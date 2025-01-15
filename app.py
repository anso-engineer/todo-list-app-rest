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

    allowed_origins = [
        "http://10.8.0.1:3000",
        "http://10.8.0.2:3000",
        "http://10.8.0.3:3000",
        "http://10.8.0.4:3000",
        "http://10.8.0.5:3000",
        "http://localhost:3000",
    ]

    # Enable CORS with hardcoded allowed origins
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": allowed_origins}})

    return app

