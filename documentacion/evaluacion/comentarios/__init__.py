# Hace que la carpeta sea un paquete válido
# y que se pueda importar el módulo desde otro lugar.
from flask import Blueprint

comentarios_bp = Blueprint('comentarios', __name__)

# Importa las rutas para registrar en el blueprint
from . import routes