from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from documentacion.evaluacion.extensions import db
from documentacion.evaluacion.models import Curso, User

# Ajusta este valor al ID que uses para el rol "docente" en tu BD
DOCENTE_ROLE_ID = 2

cursos_bp = Blueprint("cursos_bp", __name__, url_prefix="/api/cursos")

@cursos_bp.route("", methods=["POST"])
def crear_curso():
    data = request.get_json() or {}
    nombre       = data.get("nombre")
    docentes_ids = data.get("docentes", [])  # lista de user_id de docentes

    if not nombre:
        return jsonify({"error": "El nombre es obligatorio"}), 400

    curso = Curso(nombre=nombre)
    # Asociar solo usuarios con rol docente
    for did in docentes_ids:
        u = User.query.filter_by(id=did, role_id=DOCENTE_ROLE_ID).first()
        if u:
            curso.docentes.append(u)

    db.session.add(curso)
    db.session.commit()
    return jsonify({"mensaje": "Curso creado", "id": curso.id}), 201

@cursos_bp.route("", methods=["GET"])
def listar_cursos():
    # Carga los cursos junto con sus docentes (usuarios)
    cursos = Curso.query.options(
        joinedload(Curso.docentes)
    ).all()

    resultado = []
    for c in cursos:
        resultado.append({
            "id": c.id,
            "nombre": c.nombre,
            "docentes": [
                {
                    "id": u.id,
                    "username": u.username,
                    "nombre": f"{u.first_name or ''} {u.last_name or ''}".strip()
                }
                for u in c.docentes
            ]
        })
    return jsonify(resultado), 200
