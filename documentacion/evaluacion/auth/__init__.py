"""Main application package."""
from flask_jwt_extended import JWTManager
from flask import Flask

jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    ...
    app.config["JWT_SECRET_KEY"] = "HCqacbibdaja64kQ07y8hyj_Ra55ugXQgpz4bCodOpE"  # Usa algo más seguro en producción
    
    jwt.init_app(app)
    
    return app
