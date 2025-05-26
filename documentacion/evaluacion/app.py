# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask, render_template, send_from_directory, request, jsonify
from documentacion.evaluacion import commands, public, user
from documentacion.evaluacion.extensions import (
    bcrypt,
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    flask_static_digest,
    login_manager,
    migrate,
)

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from documentacion.evaluacion import settings
from documentacion.evaluacion.comentarios import comentarios_bp




app = Flask(__name__)

@app.route('/imagenes/<path:filename>')
def imagenes(filename):
    return send_from_directory('evaluacion/templates/imagenes', filename)

def create_app(config_object="evaluacion.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    CORS(app)
    app.config.from_object(config_object)
    app.config.from_object(settings)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
        
    
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    
    
    from evaluacion.evaluaciones.routes import evaluaciones_bp
    app.register_blueprint(evaluaciones_bp)
    
    from evaluacion.docentes.routes import docentes_bp
    app.register_blueprint(docentes_bp)

    from evaluacion.cursos.routes import cursos_bp
    app.register_blueprint(cursos_bp)
    
    from evaluacion.dashboard.routes import dashboard_bp
    app.register_blueprint(dashboard_bp)
    
    from evaluacion.reportes.routes import reportes_bp
    app.register_blueprint(reportes_bp)

    
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


if __name__ == "__main__":
    app.run(debug=True)