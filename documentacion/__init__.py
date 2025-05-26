# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from . import settings  # Importamos directamente el settings desde el mismo paquete
# from evaluacion.extensions import db, migrate
# from flask_jwt_extended import JWTManager


# def create_app():
#     print("create_app() ejecutado")
#     app = Flask(__name__)
    
#     # Configuración general del proyecto desde settings.py
#     app.config.from_object(settings)

#     # Inicialización de extensiones
#     db.init_app(app)
#     migrate.init_app(app, db)
    
#     # Inicialización de JWTManager
#     jwt = JWTManager()
#     jwt.init_app(app)

#     # Registrar Blueprints
#     from evaluacion.comentarios.routes import comentarios_bp
#     from evaluacion.reportes.routes import reportes_bp
#     from evaluacion.evaluaciones.routes import evaluaciones_bp
#     from evaluacion.cursos.routes import cursos_bp
#     from evaluacion.auth.routes import auth_bp

#     app.register_blueprint(comentarios_bp)
#     app.register_blueprint(reportes_bp)
#     app.register_blueprint(evaluaciones_bp)
#     app.register_blueprint(cursos_bp)
#     app.register_blueprint(auth_bp, url_prefix="/api/auth")
#     print("Blueprint de autenticación registrado correctamente en /api/auth")


#     return app

