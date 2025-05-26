# documentacion/evaluacion/comentarios/routes.py

from flask import Blueprint, request, jsonify
from documentacion.evaluacion.extensions import db
from documentacion.evaluacion.models import Comentario

comentarios_bp = Blueprint("comentarios_bp", __name__, url_prefix="/api/comentarios")

@comentarios_bp.route("", methods=["GET"])
def listar_comentarios():
    comentarios = Comentario.query.all()
    if not comentarios:
        print("❌ No hay comentarios")
        return jsonify([]), 200
    return jsonify([
        {
            "id":            c.id,
            "evaluacion_id": c.evaluacion_id,
            "tipo":          c.tipo,
            "texto":         c.texto,
            "sentimiento":   c.sentimiento,
            "fecha":         c.fecha.isoformat()
        }
        for c in comentarios
    ]),200

@comentarios_bp.route("", methods=["POST"])
def crear_comentario():
    data = request.get_json()
    if not all(k in data for k in ("evaluacion_id","tipo","texto")):
        return jsonify({"error":"Datos incompletos"}),400

    c = Comentario(
        evaluacion_id = data["evaluacion_id"],
        tipo          = data["tipo"],
        texto         = data["texto"],
        sentimiento   = data.get("sentimiento")  # opcional si ya vienes de NLP externo
    )
    db.session.add(c)
    db.session.commit()
    return jsonify({"mensaje":"✅ Comentario creado","id":c.id}),201
