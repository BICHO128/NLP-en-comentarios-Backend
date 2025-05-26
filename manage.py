import os
import sys

# 1) Aseguramos que la carpeta BACKEND esté en sys.path
sys.path.insert(0, os.path.dirname(__file__))

# 2) Importamos tu factory y extensiones
from documentacion.evaluacion import create_app
from documentacion.evaluacion.extensions import db, migrate

# 3) Creamos la app
app = create_app()

# 4) (Opcional) puedes exponer db y migrate para la shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'migrate': migrate, 'app': app}

if __name__ == '__main__':
    app.run(debug=True)
