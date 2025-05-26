# # Crea el archivo en: C:\PROYECTO DE NLP\BACKEND\evaluacion\evaluacion\reportes\excel_utils.py

# from openpyxl import Workbook
# from openpyxl.styles import Font, Alignment, PatternFill
# from io import BytesIO
# from documentacion.evaluacion.models import Evaluacion, Docente, Curso
# from sqlalchemy import func
# from documentacion.evaluacion.extensions import db


# def generar_excel_reporte(docente_id, curso_id):
#     docente = Docente.query.get_or_404(docente_id)
#     curso = Curso.query.get_or_404(curso_id)

#     evaluaciones = Evaluacion.query.filter_by(docente_id=docente_id, curso_id=curso_id).all()
#     if not evaluaciones:
#         return None

#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Evaluación Docente"

#     # Estilos
#     titulo_font = Font(size=14, bold=True)
#     header_font = Font(bold=True)
#     center = Alignment(horizontal="center")
#     azul_header = PatternFill(start_color="BDD7EE", end_color="BDD7EE", fill_type="solid")

#     # Título
#     ws.merge_cells('A1:E1')
#     ws["A1"] = f"Reporte de Evaluaciones"
#     ws["A1"].font = titulo_font
#     ws["A1"].alignment = center

#     ws.merge_cells('A2:E2')
#     ws["A2"] = f"Docente: {docente.nombre} | Curso: {curso.nombre}"
#     ws["A2"].alignment = center

#     # Encabezados
#     headers = ["Criterio", "Calificación", "Nota (1 a 5)", "Comentario Docente", "Comentario Curso"]
#     ws.append(headers)
#     for col in range(1, len(headers) + 1):
#         cell = ws.cell(row=3, column=col)
#         cell.font = header_font
#         cell.fill = azul_header
#         cell.alignment = center

#     criterios = [
#         "satisfaccion_general", "metodologia", "comunicacion", "material_didactico",
#         "puntualidad", "respeto", "organizacion", "claridad", "retroalimentacion", "disponibilidad"
#     ]

#     notas_mapeo = {
#         "Excelente": 5,
#         "Bueno": 4,
#         "Buena": 4,
#         "Regular": 3,
#         "Mala": 2,
#         "Malo": 2,
#     }

#     total_notas = 0
#     total_criterios = 0
#     fila = 4
#     for evaluacion in evaluaciones:
#         for criterio in criterios:
#             calif = getattr(evaluacion, criterio)
#             nota = notas_mapeo.get(calif, 1)
#             total_notas += nota
#             total_criterios += 1

#             ws.append([
#                 criterio.replace("_", " ").capitalize(),
#                 calif,
#                 nota,
#                 evaluacion.comentario_docente if criterio == "satisfaccion_general" else "",
#                 evaluacion.comentario_curso if criterio == "satisfaccion_general" else "",
#             ])
#             fila += 1

#     nota_final = round(total_notas / total_criterios, 2) if total_criterios else 0

#     ws.append([])
#     ws.append(["Nota Final Promedio", nota_final])

#     output = BytesIO()
#     wb.save(output)
#     output.seek(0)
#     return output
