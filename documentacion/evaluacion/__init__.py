from flask import Flask
from documentacion.evaluacion.settings import settings  # Importamos directamente el settings desde el mismo paquete ( si algo no funciona, revisar esta línea, agregar la ruta completa si es necesario)
# from documentacion.evaluacion import settings
from documentacion.evaluacion.extensions import db, migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

# db = SQLAlchemy()
# migrate = Migrate()

def create_app():
    print("create_app() ejecutado")
    app = Flask(__name__)
    
    # CORS - Configuración mejorada para manejar ambas rutas
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, 
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )
    # CORS(app, 
    #      resources={r"/api/*": {
    #          "origins": [
    #              "http://localhost:5173",
    #              "http://127.0.0.1:5173"
    #          ]
    #      }}, 
    #      supports_credentials=True,
    #      allow_headers=["Content-Type", "Authorization"],
    #      methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    # )


    
    # Configuración general del proyecto desde settings.py
    app.config.from_object(settings)

    # Inicialización de extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Inicialización de JWTManager
    jwt = JWTManager()
    jwt.init_app(app)

    # Registrar Blueprints
    from documentacion.evaluacion.comentarios.routes import comentarios_bp
    from documentacion.evaluacion.reportes.routes import reportes_bp
    from documentacion.evaluacion.evaluaciones.routes import evaluaciones_bp
    from documentacion.evaluacion.cursos.routes import cursos_bp
    from documentacion.evaluacion.auth.routes import auth_bp
    from documentacion.evaluacion.docentes.routes import docentes_bp
    from documentacion.evaluacion.admin.routes import admin_bp
    # from documentacion.evaluacion.dashboard.routes import dashboard_bp
    
    
    # app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(docentes_bp)
    app.register_blueprint(comentarios_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(evaluaciones_bp)
    app.register_blueprint(cursos_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    print("Blueprint de autenticación registrado correctamente en /api/auth")


    return app

