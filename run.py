import sys
import os
import warnings

warnings.filterwarnings("ignore")

# Agrega la carpeta documentacion al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'documentacion'))

from evaluacion import create_app

app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
    
