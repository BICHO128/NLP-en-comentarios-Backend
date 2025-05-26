# documentacion/evaluacion/docentes/routes.py

from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from documentacion.evaluacion.extensions import db
from documentacion.evaluacion.models import User, Docente, Role

docentes_bp = Blueprint("docentes_bp", __name__, url_prefix="/api/docentes")

@docentes_bp.route("", methods=["GET"])
def listar_docentes():
    docentes = Docente.query.options(joinedload(Docente.user)).all()
    return jsonify([
        {
            "id":       d.docente_id,
            "username": d.user.username,
            "nombre":   f"{d.user.first_name or ''} {d.user.last_name or ''}".strip()
        }
        for d in docentes
    ]), 200

@docentes_bp.route("", methods=["POST"])
def crear_docente():
    data = request.get_json()
    u = User(
        username   = data.get("username"),
        email      = data.get("email"),
        first_name = data.get("first_name"),
        last_name  = data.get("last_name"),
        role_id    = Role.query.filter_by(name="docente").first().id
    )
    u.password = data.get("password")  # setter hashea
    db.session.add(u)
    db.session.flush()  # necesita u.id

    doc = Docente(docente_id=u.id)
    db.session.add(doc)
    db.session.commit()
    return jsonify({"mensaje": "Docente creado", "id": doc.docente_id}), 201

@docentes_bp.route("/<int:docente_id>/cursos", methods=["GET"])
def cursos_por_docente(docente_id):
    d = Docente.query.options(joinedload(Docente.cursos)).get_or_404(docente_id)
    return jsonify([
        {"id": c.id,
         "username": d.user.username,
         "nombre": c.nombre}
        for c in d.cursos
    ]), 200
