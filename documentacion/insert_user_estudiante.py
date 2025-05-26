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
        username="David Urrutia Ceron",
        email="david.urrutia.c@uniautonoma.edu.co",
        created_at=datetime.now(),
        first_name="David",
        last_name="Urrutia Ceron",
        active=True,
        is_admin=False,
        id= 6
        
    )

    # Aquí se usa el setter que aplica bcrypt
    usuario.password = "123"
    

    db.session.add(usuario)
    db.session.commit()
    
    #####################################

    # Crear el usuario utilizando el setter del modelo para el password
    usuario = User(
        username="Deiby Alejandro Ramirez Galvis",
        email="deiby.ramirez.g@uniautonoma.edu.co",
        created_at=datetime.now(),
        first_name="Deiby Alejandro",
        last_name="Ramirez Galvis",
        active=True,
        is_admin=False,
        id= 7 
    )
               

    # Aquí se usa el setter que aplica bcrypt
    usuario.password = "123"
    

    db.session.add(usuario)
    db.session.commit()
    
    #####################################
    
     # Crear el usuario utilizando el setter del modelo para el password
    usuario = User(
        username="Thomas Montoya Magon",
        email="thomas.montoya.m@uniautonoma.edu.co",
        created_at=datetime.now(),
        first_name="Thomas",
        last_name="Montoya Magon",
        active=True,
        is_admin=False,
        id= 8
        
    )
    
    # Aquí se usa el setter que aplica bcrypt
    usuario.password = "123"
    

    db.session.add(usuario)
    db.session.commit()
    
    #####################################
    
     # Crear el usuario utilizando el setter del modelo para el password
    usuario = User(
        username="Luisa Jhulieth Joaqui Jimenez",
        email="luisa.joaqui.j@uniautonoma.edu.co",
        created_at=datetime.now(),
        first_name="Luisa Jhulieth",
        last_name="Joaqui Jimenez",
        active=True,
        is_admin=False,
        id= 9
        
    )
    
    # Aquí se usa el setter que aplica bcrypt
    usuario.password = "123"
    

    db.session.add(usuario)
    db.session.commit()
    
    #####################################
    
     # Crear el usuario utilizando el setter del modelo para el password
    usuario = User(
        username="Daviel Rivas Agredo",
        email="daniel.rivas.a@uniautonoma.edu.co",
        created_at=datetime.now(),
        first_name="Daniel",
        last_name="Rivas Agredo",
        active=True,
        is_admin=False,
        id= 10
        
    )
    
    # Aquí se usa el setter que aplica bcrypt
    usuario.password = "123"
    

    db.session.add(usuario)
    db.session.commit()


    print("✅ Usuarios docentes creado con éxito con contraseña encriptada (bcrypt)")
