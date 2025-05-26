# from flask import Blueprint, jsonify
# from sqlalchemy.orm import joinedload
# from documentacion.evaluacion.extensions import db
# from documentacion.evaluacion.models import Evaluacion, Docente, Curso
# from collections import defaultdict

# # Blueprint con prefijo /api/dashboard
# dashboard_bp = Blueprint('dashboard_bp', __name__, url_prefix='/api/dashboard')

# @dashboard_bp.route('/admin', methods=['GET'])
# def dashboard_admin_global():
#     """
#     Resumen global: por docente y por curso, con conteos de criterios, sentimientos y comentarios.
#     Maneja el caso de que no haya evaluaciones.
#     """
#     evaluaciones = Evaluacion.query.all()
#     if not evaluaciones:
#         return jsonify({"mensaje": "No hay evaluaciones registradas."}), 200

#     resumen = defaultdict(lambda: defaultdict(lambda: {
#         'total_evaluaciones': 0,
#         'resumen_criterios': defaultdict(int),
#         'sentimientos_docente': defaultdict(int),
#         'sentimientos_curso': defaultdict(int),
#         'comentarios': []
#     }))

#     for ev in evaluaciones:
#         # keys
#         nombre_doc = f"{ev.docente.user.first_name or ''} {ev.docente.user.last_name or ''}".strip()
#         nombre_cur = ev.curso.nombre if ev.curso else 'Curso Desconocido'
#         dato = resumen[nombre_doc][nombre_cur]
#         dato['total_evaluaciones'] += 1

#         # calificaciones pivot
#         for cal in ev.calificaciones:
#             clave = cal.criterio.descripcion
#             dato['resumen_criterios'][clave] += cal.valor

#         # sentimientos y comentarios
#         for cm in ev.comentarios:
#             if cm.tipo == 'docente':
#                 dato['sentimientos_docente'][cm.sentimiento] += 1
#             else:
#                 dato['sentimientos_curso'][cm.sentimiento] += 1
#             dato['comentarios'].append({
#                 'tipo': cm.tipo,
#                 'texto': cm.texto,
#                 'sentimiento': cm.sentimiento,
#                 'fecha': cm.fecha.isoformat()
#             })

#     # convertir defaultdict a dict
#     def to_dict(d):
#         if isinstance(d, defaultdict):
#             return {k: to_dict(v) for k, v in d.items()}
#         if isinstance(d, dict):
#             return {k: to_dict(v) for k, v in d.items()}
#         return d

#     return jsonify(to_dict(resumen)), 200

# @dashboard_bp.route('/docente/<int:docente_id>', methods=['GET'])
# def dashboard_por_docente(docente_id):
#     """
#     Resumen por docente: agrupa por curso con criterios, sentimientos y comentarios.
#     Maneja el caso sin evaluaciones.
#     """
#     docente = Docente.query.options(joinedload(Docente.user)).get_or_404(docente_id)
#     evs = Evaluacion.query.filter_by(docente_id=docente_id).all()
#     if not evs:
#         return jsonify({
#             'docente': f"{docente.user.first_name or ''} {docente.user.last_name or ''}".strip(),
#             'cursos': []
#         }), 200

#     resumen = defaultdict(lambda: {
#         'total_evaluaciones': 0,
#         'resumen_criterios': defaultdict(int),
#         'sentimientos_docente': defaultdict(int),
#         'sentimientos_curso': defaultdict(int),
#         'comentarios_docente': [],
#         'comentarios_curso': []
#     })

#     for ev in evs:
#         curso_nombre = ev.curso.nombre if ev.curso else 'Curso Desconocido'
#         dato = resumen[curso_nombre]
#         dato['total_evaluaciones'] += 1
#         # calificaciones
#         for cal in ev.calificaciones:
#             clave = cal.criterio.descripcion
#             dato['resumen_criterios'][clave] += cal.valor
#         # comentarios y sentimientos
#         for cm in ev.comentarios:
#             if cm.tipo == 'docente':
#                 dato['sentimientos_docente'][cm.sentimiento] += 1
#                 dato['comentarios_docente'].append({'texto': cm.texto, 'sentimiento': cm.sentimiento})
#             else:
#                 dato['sentimientos_curso'][cm.sentimiento] += 1
#                 dato['comentarios_curso'].append({'texto': cm.texto, 'sentimiento': cm.sentimiento})

#     # formatear salida
#     resultado = {
#         'docente': f"{docente.user.first_name or ''} {docente.user.last_name or ''}".strip(),
#         'cursos': []
#     }
#     for curso, dato in resumen.items():
#         sent_doc = max(dato['sentimientos_docente'], key=dato['sentimientos_docente'].get) if dato['sentimientos_docente'] else None
#         sent_cur = max(dato['sentimientos_curso'], key=dato['sentimientos_curso'].get)   if dato['sentimientos_curso'] else None
#         resultado['cursos'].append({
#             'curso': curso,
#             'total_evaluaciones': dato['total_evaluaciones'],
#             'resumen_sentimiento_docente': sent_doc,
#             'resumen_sentimiento_curso': sent_cur,
#             'resumen_criterios': [{ 'criterio': crit, 'cantidad': count } for crit, count in dato['resumen_criterios'].items()],
#             'comentarios_docente': dato['comentarios_docente'],
#             'comentarios_curso': dato['comentarios_curso']
#         })

#     return jsonify(resultado), 200

# @dashboard_bp.route('/docente/<int:docente_id>/curso/<int:curso_id>', methods=['GET'])
# def dashboard_docente_por_curso(docente_id, curso_id):
#     """
#     Resumen detallado para un docente y curso específico.
#     Maneja el caso sin evaluaciones o curso no asignado.
#     """
#     docente = Docente.query.options(joinedload(Docente.user)).get_or_404(docente_id)
#     curso = Curso.query.get_or_404(curso_id)
#     # validar relación M:N
#     if not any(d.user_id == docente_id for d in curso.docentes):
#         return jsonify({'error': 'Curso no asignado a este docente'}), 400

#     evs = Evaluacion.query.filter_by(docente_id=docente_id, curso_id=curso_id).all()
#     if not evs:
#         return jsonify({
#             'docente': docente.user.username,
#             'curso': curso.nombre,
#             'total_evaluaciones': 0
#         }), 200

#     # reutilizar lógica de dashboard_por_docente y filtrar
#     data = dashboard_por_docente(docente_id).get_json()
#     for c in data['cursos']:
#         if c['curso'] == curso.nombre:
#             return jsonify(c), 200
#     return jsonify({'error': 'Datos no encontrados'}), 404

