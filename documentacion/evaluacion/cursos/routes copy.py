# documentacion/evaluacion/cursos/routes.py

from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from documentacion.evaluacion.extensions import db
from documentacion.evaluacion.models import Curso, Docente

cursos_bp = Blueprint("cursos_bp", __name__, url_prefix="/api/cursos")

@cursos_bp.route("", methods=["POST"])
def crear_curso():
    data = request.get_json()
    nombre       = data.get("nombre")
    docentes_ids = data.get("docentes", [])  # lista de user_id de docentes

    if not nombre:
        return jsonify({"error": "El nombre es obligatorio"}), 400

    curso = Curso(nombre=nombre)
    # Asociar docentes
    for did in docentes_ids:
        d = Docente.query.get(did)
        if d:
            curso.docentes.append(d)

    db.session.add(curso)
    db.session.commit()
    return jsonify({"mensaje": "Curso creado", "id": curso.id}), 201

@cursos_bp.route("", methods=["GET"])
def listar_cursos():
    cursos = Curso.query.options(
        joinedload(Curso.docentes).joinedload(Docente.user)
    ).all()
    resultado = []
    for c in cursos:
        resultado.append({
            "id":     c.id,
            "nombre": c.nombre,
            "docentes": [
                {
                    "id":        d.user_id,
                    "username":  d.user.username,
                    "nombre":    f"{d.user.first_name or ''} {d.user.last_name or ''}".strip()
                }
                for d in c.docentes
            ]
        })
    return jsonify(resultado), 200
