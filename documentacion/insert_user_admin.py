import os
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash

# Agrega la ruta del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from documentacion.evaluacion import create_app, db
from documentacion.evaluacion.models import User

app = create_app()

with app.app_context():
    admin_email = "admin@uniautonoma.edu.co"

    existente = User.query.filter_by(email=admin_email).first()
    if existente:
        print("🛑 Ya existe un usuario con ese correo. Eliminando para reinserción...")
        db.session.delete(existente)
        db.session.commit()

    password_hash = generate_password_hash("123")

    admin = User(
        id=11,  # Usa un ID nuevo que no esté ocupado
        username="admin",
        email=admin_email,
        password=password_hash,
        created_at=datetime.now(),
        first_name="Admin",
        last_name="Principal",
        is_admin=True,
        active=True
    )

    db.session.add(admin)
    db.session.commit()
    print("✅ Administrador insertado correctamente.")
