import sys
import os
from datetime import datetime

# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from documentacion.evaluacion import create_app, db
from documentacion.evaluacion.models import User  # Usa tu modelo User que tiene el setter con bcrypt

app = create_app()

with app.app_context():
    
    # Crear el usuario utilizando el setter del modelo para el password
    usuario = User(
        username="Ana Maria Caviedes Castillo",
        email="ana.caviedes.c@uniautonoma.edu.co",
        created_at=datetime.now(),
        first_name="Ana Maria",
        last_name="Caviedes Castillo",
        active=True,
        is_admin=False,
        id= 1
        
    )

    # Aquí se usa el setter que aplica bcrypt
    usuario.password = "123"
    

    db.session.add(usuario)
    db.session.commit()
    
    #####################################

    # Crear el usuario utilizando el setter del modelo para el password
    usuario = User(
        username="Jose Fernando Concha Gonzalez",
        email="jose.concha.g@uniautonoma.edu.co",
        created_at=datetime.now(),
        first_name="Jose Fernando",
        last_name="Concha Gonzalez",
        active=True,
        is_admin=False,
        id= 2
        
    )

    # Aquí se usa el setter que aplica bcrypt
    usuario.password = "123"
    

    db.session.add(usuario)
    db.session.commit()
    
    #####################################
    
     # Crear el usuario utilizando el setter del modelo para el password
    usuario = User(
        username="Ana Gabriela Fernandez Morantes",
        email="ana.fernandez.m@uniautonoma.edu.co",
        created_at=datetime.now(),
        first_name="Ana Gabriela",
        last_name="Fernandez Morantes",
        active=True,
        is_admin=False,
        id= 3
        
    )

    # Aquí se usa el setter que aplica bcrypt
    usuario.password = "123"
    
    db.session.add(usuario)
    db.session.commit()
    
    #####################################

    
     # Crear el usuario utilizando el setter del modelo para el password
    usuario = User(
        username="Diego Fernando Prado Osorios",
        email="diego.prado.o@uniautonoma.edu.co",
        created_at=datetime.now(),
        first_name="Diego Fernando",
        last_name="Prado Osorios",
        active=True,
        is_admin=False,
        id= 4
        
    )

    # Aquí se usa el setter que aplica bcrypt
    usuario.password = "123"
    
    db.session.add(usuario)
    db.session.commit()
    
    #####################################

    
     # Crear el usuario utilizando el setter del modelo para el password
    usuario = User(
        username="Diana Patricia Garzon Muñoz",
        email="diana.garzon.m@uniautonoma.edu.co",
        created_at=datetime.now(),
        first_name="Diana Patricia",
        last_name="Garzon Muñoz",
        active=True,
        is_admin=False,
        id= 5
        
    )

    # Aquí se usa el setter que aplica bcrypt
    usuario.password = "123"
    

    db.session.add(usuario)
    db.session.commit()

    print("✅ Usuarios docentes creado con éxito con contraseña encriptada (bcrypt)")
