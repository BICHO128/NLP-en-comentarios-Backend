from documentacion.evaluacion import create_app
from documentacion.evaluacion.models import Docente, Curso, Evaluacion
from datetime import datetime
from documentacion.evaluacion.extensions import db

app = create_app()

with app.app_context():
    # Limpiar si ya hay algo
    Evaluacion.query.delete()
    Curso.query.delete()
    Docente.query.delete()
    
    # Crear docentes
    docentes = [
        # recordar que python maneja los indices desde 0 entonces el id 0 es el primero
        # y el id 1 es el segundo y asi sucesivamente
        Docente(nombre="Ana Maria Caviedes Castillo", email="ana.caviedes.c@uniautonoma.edu.co"), #id 1
        Docente(nombre="Jose Fernando Concha Gonzalez", email="jose.concha.g@uniautonoma.edu.co"), #id 2
        Docente(nombre="Ana Gabriela Fernandez Morantes", email="ana.fernandez.m@uniautonoma.edu.co"), #id 3
        Docente(nombre="Diego Fernando Prado Osorio", email="diego.prado.o@uniautonoma.edu.co"), #id 4
        Docente(nombre="Diana Patricia Garzon Muñoz", email="diana.garzon.m@uniautonoma.edu.co") #id 5
    ]

    for d in docentes:
        db.session.add(d)

    db.session.commit()

    # Crear cursos para cada docente
    cursos = [
       Curso(nombre="Ingeniería de Software II", docente_id=docentes[0].id),  # Ana Maria
        Curso(nombre="Probabilidad y Estadística", docente_id=docentes[1].id),  # Jose
        Curso(nombre="Base de Datos II", docente_id=docentes[2].id),  # Ana Gabriela
        Curso(nombre="Desarrollo Web", docente_id=docentes[2].id),
        Curso(nombre="Base de Datos II", docente_id=docentes[3].id),  # Diego
        Curso(nombre="Complejidad Algorítmica", docente_id=docentes[3].id),
        Curso(nombre="Inglés III", docente_id=docentes[4].id)  # Diana
    ]

    for c in cursos:
        db.session.add(c)

    db.session.commit()

    # Evaluaciones (una por docente)
    evaluaciones = [
        Evaluacion(
            docente_id=docentes[0].id, curso_id=cursos[0].id,
            satisfaccion_general="Bueno", metodologia="Bueno", comunicacion="Excelente",
            material_didactico="Bueno", puntualidad="Excelente", respeto="Excelente",
            organizacion="Bueno", claridad="Bueno", retroalimentacion="Bueno", disponibilidad="Excelente",
            comentario_docente="La profesora explica con claridad y es muy organizada.",
            sentimiento_docente="positivo",
            comentario_curso="El curso fue claro y bien estructurado.",
            sentimiento_curso="positivo",
            fecha=datetime.now()
        ),
        Evaluacion(
            docente_id=docentes[1].id, curso_id=cursos[1].id,
            satisfaccion_general="Excelente", metodologia="Bueno", comunicacion="Excelente",
            material_didactico="Regular", puntualidad="Excelente", respeto="Bueno",
            organizacion="Bueno", claridad="Excelente", retroalimentacion="Bueno", disponibilidad="Regular",
            comentario_docente="El docente explica muy bien los temas.",
            sentimiento_docente="positivo",
            comentario_curso="El curso es algo difícil pero se aprende.",
            sentimiento_curso="neutral",
            fecha=datetime.now()
        ),
        Evaluacion(
            docente_id=docentes[2].id, curso_id=cursos[2].id,
            satisfaccion_general="Bueno", metodologia="Regular", comunicacion="Bueno",
            material_didactico="Excelente", puntualidad="Bueno", respeto="Bueno",
            organizacion="Excelente", claridad="Bueno", retroalimentacion="Regular", disponibilidad="Bueno",
            comentario_docente="Muy buen material y puntual en sus clases.",
            sentimiento_docente="positivo",
            comentario_curso="El contenido es avanzado pero útil.",
            sentimiento_curso="positivo",
            fecha=datetime.now()
        ),
        Evaluacion(
            docente_id=docentes[3].id, curso_id=cursos[4].id,
            satisfaccion_general="Regular", metodologia="Regular", comunicacion="Regular",
            material_didactico="Bueno", puntualidad="Excelente", respeto="Bueno",
            organizacion="Regular", claridad="Regular", retroalimentacion="Regular", disponibilidad="Bueno",
            comentario_docente="Debe mejorar su metodología.",
            sentimiento_docente="neutral",
            comentario_curso="El curso tiene buenos temas pero falta claridad.",
            sentimiento_curso="negativo",
            fecha=datetime.now()
        ),
        Evaluacion(
            docente_id=docentes[4].id, curso_id=cursos[6].id,
            satisfaccion_general="Excelente", metodologia="Excelente", comunicacion="Excelente",
            material_didactico="Excelente", puntualidad="Excelente", respeto="Excelente",
            organizacion="Excelente", claridad="Excelente", retroalimentacion="Excelente", disponibilidad="Excelente",
            comentario_docente="Una docente muy profesional y dedicada.",
            sentimiento_docente="positivo",
            comentario_curso="Excelente curso, muy dinámico y participativo.",
            sentimiento_curso="positivo",
            fecha=datetime.now()
        )
    ]

    for e in evaluaciones:
        db.session.add(e)

    db.session.commit()
    print("✅ Docentes, cursos y evaluaciones insertadas correctamente.")
