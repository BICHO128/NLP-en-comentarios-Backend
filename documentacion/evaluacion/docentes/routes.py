from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from documentacion.evaluacion.extensions import db
from documentacion.evaluacion.models import User, Curso

# Constante para el role_id de los docentes (ajusta este valor a tu configuración)
DOCENTE_ROLE_ID = 2

docentes_bp = Blueprint("docentes_bp", __name__, url_prefix="/api/docentes")

@docentes_bp.route("", methods=["GET"])
def listar_docentes():
    # Obtener todos los usuarios con rol docente
    docentes = User.query \
        .options(joinedload(User.cursos)) \
        .filter_by(role_id=DOCENTE_ROLE_ID) \
        .all()

    resultado = []
    for u in docentes:
        resultado.append({
            "id": u.id,
            "username": u.username,
            "nombre": f"{u.first_name or ''} {u.last_name or ''}".strip()
        })
    return jsonify(resultado), 200

@docentes_bp.route("", methods=["POST"])
def crear_docente():
    data = request.get_json() or {}
    # Crear usuario con rol docente
    u = User(
        username=data.get("username"),
        email=data.get("email"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        role_id=DOCENTE_ROLE_ID
    )
    u.password = data.get("password")  # setter encripta
    db.session.add(u)
    db.session.commit()

    return jsonify({"mensaje": "Docente creado", "id": u.id}), 201

@docentes_bp.route("/<int:docente_id>/cursos", methods=["GET"])
def cursos_por_docente(docente_id):
    # Obtener usuario docente y sus cursos
    u = User.query.options(joinedload(User.cursos)) \
        .filter_by(id=docente_id, role_id=DOCENTE_ROLE_ID) \
        .first_or_404()

    cursos = []
    for c in u.cursos:
        cursos.append({
            "id": c.id,
            "nombre": c.nombre
        })
    return jsonify(cursos), 200
