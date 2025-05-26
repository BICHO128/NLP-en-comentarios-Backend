# documentacion/evaluacion/evaluaciones/routes.py

from flask import Blueprint, request, jsonify
from datetime import datetime
from documentacion.evaluacion.extensions import db
from documentacion.evaluacion.models import (
    Evaluacion, Calificacion, Comentario,
    Estudiante, Docente, Curso, Criterio, User
)
from hybrid_sentiment import analizar_sentimiento

evaluaciones_bp = Blueprint("evaluaciones_bp", __name__, url_prefix="/api/evaluaciones")

@evaluaciones_bp.route("", methods=["POST"])
def crear_evaluacion():
    data = request.get_json()
    # Campos obligatorios
    required = ("estudiante_id","docente_id","curso_id","calificaciones","comentarios")
    if not all(k in data for k in required):
        return jsonify({"error":"Datos incompletos"}),400

    # Validar existencia de FK
    if not Estudiante.query.get(data["estudiante_id"]):
        return jsonify({"error":"Estudiante no existe"}),404
    if not Docente.query.get(data["docente_id"]):
        return jsonify({"error":"Docente no existe"}),404
    if not Curso.query.get(data["curso_id"]):
        return jsonify({"error":"Curso no existe"}),404

    ev = Evaluacion(
        estudiante_id = data["estudiante_id"],
        docente_id    = data["docente_id"],
        curso_id      = data["curso_id"],
        fecha         = datetime.now()
    )
    db.session.add(ev)
    db.session.flush()

    # Calificaciones
    for c in data["calificaciones"]:
        crit = Criterio.query.get(c.get("criterio_id"))
        if crit and isinstance(c.get("valor"), int):
            db.session.add(Calificacion(
                evaluacion_id = ev.id,
                criterio_id   = crit.id,
                valor         = c["valor"]
            ))

    # Comentarios
    for cm in data["comentarios"]:
        if cm.get("tipo") in ("docente","curso") and cm.get("texto"):
            resultado = analizar_sentimiento(cm["texto"])
            # resultado es dict → nos quedamos sólo con la cadena
            sentimiento_str = resultado.get("final") if isinstance(resultado, dict) else str(resultado)
            db.session.add(Comentario(
                evaluacion_id = ev.id,
                tipo          = cm["tipo"],
                texto         = cm["texto"],
                sentimiento   = sentimiento_str,
                fecha         = datetime.now()
            ))

    db.session.commit()
    return jsonify({"mensaje":"Evaluación creada","id":ev.id}),201

def _serializar(ev):
    return {
        "id": ev.id,
        "estudiante_id": ev.estudiante_id,
        "docente_id": ev.docente_id,
        "curso_id": ev.curso_id,
        "docente": ev.docente.user.first_name+" "+ev.docente.user.last_name,
        "curso": ev.curso.nombre,
        "fecha": ev.fecha.isoformat(),
        "calificaciones": [
            {"criterio": cal.criterio.descripcion, "valor": cal.valor}
            for cal in ev.calificaciones
        ],
        "comentarios": [
            {"tipo": cm.tipo, "texto": cm.texto, "sentimiento": cm.sentimiento}
            for cm in ev.comentarios
        ]
    }

@evaluaciones_bp.route("", methods=["GET"])
def listar_evaluaciones():
    all_evs = Evaluacion.query.all()
    if not all_evs:
        print("❌No hay evaluaciones")
    return jsonify([_serializar(ev) for ev in all_evs]),200

@evaluaciones_bp.route("/docente/<int:docente_id>", methods=["GET"])
def por_docente(docente_id):
    evs = Evaluacion.query.filter_by(docente_id=docente_id).all()
    if not evs:
        print("❌No hay evaluaciones")
    return jsonify([_serializar(ev) for ev in evs]),200

@evaluaciones_bp.route("/docente/<int:docente_id>/curso/<int:curso_id>", methods=["GET"])
def por_docente_y_curso(docente_id, curso_id):
    evs = Evaluacion.query.filter_by(docente_id=docente_id, curso_id=curso_id).all()
    if not evs:
        print("❌No hay evaluaciones")
    return jsonify([_serializar(ev) for ev in evs]),200


# Devuelve todos los docentes con sus cursos (para el Admin)
@evaluaciones_bp.route('/docentes-con-cursos', methods=['GET'])
def docentes_con_cursos():
    resultado = []
    for d in Docente.query.all():
        # Docente usa user_id como PK y relación a User
        usuario = User.query.get_or_404(d.user_id)
        nombre = f"{usuario.first_name} {usuario.last_name}"
        cursos = [{'id': c.id, 'nombre': c.nombre} for c in d.cursos]
        resultado.append({
            'docente_id': d.user_id,
            'nombre': nombre,
            'cursos': cursos
        })
    return jsonify(resultado), 200

