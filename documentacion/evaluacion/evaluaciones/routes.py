from flask import Blueprint, request, jsonify
from datetime import datetime
from sqlalchemy.orm import joinedload
from documentacion.evaluacion.extensions import db
from documentacion.evaluacion.models import (
    Evaluacion, Calificacion, Comentario,
    Curso, Criterio, User
)
from hybrid_sentiment import analizar_sentimiento

# Constantes para roles
DOCENTE_ROLE_ID = 2
ESTUDIANTE_ROLE_ID = 1  # ajusta según tu config

evaluaciones_bp = Blueprint(
    "evaluaciones_bp", __name__, url_prefix="/api/evaluaciones"
)

@evaluaciones_bp.route("", methods=["POST"])
def crear_evaluacion():
    data = request.get_json() or {}
    # Campos obligatorios
    required = ("estudiante_id", "docente_id", "curso_id", "calificaciones", "comentarios")
    if not all(k in data for k in required):
        return jsonify({"error": "Datos incompletos"}), 400

    # Validar existencia de FK como User con roles
    est = User.query.filter_by(id=data["estudiante_id"], role_id=ESTUDIANTE_ROLE_ID).first()
    if not est:
        return jsonify({"error": "Estudiante no existe"}), 404
    doc = User.query.filter_by(id=data["docente_id"], role_id=DOCENTE_ROLE_ID).first()
    if not doc:
        return jsonify({"error": "Docente no existe"}), 404
    cur = Curso.query.get(data["curso_id"])
    if not cur:
        return jsonify({"error": "Curso no existe"}), 404

    ev = Evaluacion(
        estudiante_id=est.id,
        docente_id=doc.id,
        curso_id=cur.id,
        fecha=datetime.utcnow()
    )
    db.session.add(ev)
    db.session.flush()

    # Calificaciones
    for c in data["calificaciones"]:
        crit = Criterio.query.get(c.get("criterio_id"))
        if crit and isinstance(c.get("valor"), int):
            db.session.add(Calificacion(
                evaluacion_id=ev.id,
                criterio_id=crit.id,
                valor=c["valor"]
            ))

    # Comentarios
    for cm in data["comentarios"]:
        if cm.get("tipo") in ("docente", "curso") and cm.get("texto"):
            resultado = analizar_sentimiento(cm["texto"])
            sentimiento_str = resultado.get("final") if isinstance(resultado, dict) else str(resultado)
            db.session.add(Comentario(
                evaluacion_id=ev.id,
                tipo=cm["tipo"],
                texto=cm["texto"],
                sentimiento=sentimiento_str,
                fecha=datetime.utcnow()
            ))

    db.session.commit()
    return jsonify({"mensaje": "Evaluación creada", "id": ev.id}), 201


def _serializar(ev):
    # Nombre completo de docente y estudiante
    nombre_doc = f"{ev.docente.first_name or ''} {ev.docente.last_name or ''}".strip()
    nombre_est = f"{ev.estudiante.first_name or ''} {ev.estudiante.last_name or ''}".strip()
    return {
        "id": ev.id,
        "estudiante_id": ev.estudiante_id,
        "docente_id": ev.docente_id,
        "curso_id": ev.curso_id,
        "estudiante": nombre_est,
        "docente": nombre_doc,
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
    evs = Evaluacion.query.options(
        joinedload(Evaluacion.calificaciones),
        joinedload(Evaluacion.comentarios),
        joinedload(Evaluacion.curso),
        joinedload(Evaluacion.docente),
        joinedload(Evaluacion.estudiante)
    ).all()
    return jsonify([_serializar(ev) for ev in evs]), 200

@evaluaciones_bp.route("/docente/<int:docente_id>", methods=["GET"])
def por_docente(docente_id):
    evs = Evaluacion.query.filter_by(docente_id=docente_id).all()
    return jsonify([_serializar(ev) for ev in evs]), 200

@evaluaciones_bp.route("/docente/<int:docente_id>/curso/<int:curso_id>", methods=["GET"])
def por_docente_y_curso(docente_id, curso_id):
    evs = Evaluacion.query.filter_by(
        docente_id=docente_id,
        curso_id=curso_id
    ).all()
    return jsonify([_serializar(ev) for ev in evs]), 200

@evaluaciones_bp.route("/docentes-con-cursos", methods=["GET"])
def docentes_con_cursos():
    # Listar todos los usuarios con rol docente y sus cursos
    docentes = User.query.options(joinedload(User.cursos)) \
                     .filter_by(role_id=DOCENTE_ROLE_ID).all()
    resultado = []
    for u in docentes:
        cursos = [{"id": c.id, "nombre": c.nombre} for c in u.cursos]
        resultado.append({
            "docente_id": u.id,
            "nombre": f"{u.first_name or ''} {u.last_name or ''}".strip(),
            "cursos": cursos
        })
    return jsonify(resultado), 200
