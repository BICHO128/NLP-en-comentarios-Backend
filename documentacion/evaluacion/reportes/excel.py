from io import BytesIO
import pandas as pd
from flask import send_file
from documentacion.evaluacion.models import Evaluacion, User, Curso

def generar_excel_reporte(docente_user: User, curso: Curso, evaluaciones):
    

    if not docente_user or not curso or not evaluaciones:
        return None

    # Preparar datos para DataFrame
    datos = []
    for e in evaluaciones:
        criterios = [
            ("Satisfacción General", e.satisfaccion_general),
            ("Metodología", e.metodologia),
            ("Comunicación", e.comunicacion),
            ("Material Didáctico", e.material_didactico),
            ("Puntualidad", e.puntualidad),
            ("Respeto", e.respeto),
            ("Organización", e.organizacion),
            ("Claridad", e.claridad),
            ("Retroalimentación", e.retroalimentacion),
            ("Disponibilidad", e.disponibilidad)
        ]

        for criterio, valor in criterios:
            nota = calcular_nota(valor)
            datos.append({
                "Criterio": criterio,
                "Calificación": valor,
                "Nota": nota
            })

    df = pd.DataFrame(datos)
    promedio_final = df["Nota"].mean().round(2)

    # Crear Excel
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Evaluaciones')

    # Agregar resumen y comentarios
    workbook = writer.book
    worksheet = writer.sheets['Evaluaciones']

    worksheet.write('E2', 'User:')
    nombre_completo = f"{docente_user.first_name} {docente_user.last_name}"
    worksheet.write('F2', nombre_completo)

    worksheet.write('E3', 'Curso:')
    worksheet.write('F3', curso.nombre)
    worksheet.write('E4', 'Promedio Final:')
    worksheet.write('F4', promedio_final)

    fila = len(df) + 6
    worksheet.write(f'B{fila}', 'Comentarios sobre el User:')
    for eval in evaluaciones:
        fila += 1
        worksheet.write(f'B{fila}', eval.comentario_User)

    fila += 2
    worksheet.write(f'B{fila}', 'Comentarios sobre el curso:')
    for eval in evaluaciones:
        fila += 1
        worksheet.write(f'B{fila}', eval.comentario_curso)

    writer.close()
    output.seek(0)

    return send_file(output, download_name=f"reporte_{User.nombre}_{curso.nombre}.xlsx", as_attachment=True)

def calcular_nota(valor):
    mapeo = {
        "Excelente": 5.0,
        "Bueno": 4.0,
        "Regular": 3.0,
        "Malo": 2.0,
        "Pésimo": 1.0
    }
    return mapeo.get(valor, 0.0)




def generar_excel_admin():
    from evaluacion.models import Evaluacion, User, Curso

    evaluaciones = Evaluacion.query.all()
    if not evaluaciones:
        return None

    datos = []
    for eval in evaluaciones:
        User = User.query.get(eval.User_id)
        curso = Curso.query.get(eval.curso_id)

        criterios = [
            ("Satisfacción General", eval.satisfaccion_general),
            ("Metodología", eval.metodologia),
            ("Comunicación", eval.comunicacion),
            ("Material Didáctico", eval.material_didactico),
            ("Puntualidad", eval.puntualidad),
            ("Respeto", eval.respeto),
            ("Organización", eval.organizacion),
            ("Claridad", eval.claridad),
            ("Retroalimentación", eval.retroalimentacion),
            ("Disponibilidad", eval.disponibilidad)
        ]

        for criterio, valor in criterios:
            nota = calcular_nota(valor)
            datos.append({
                "User": User.nombre,
                "Curso": curso.nombre,
                "Criterio": criterio,
                "Calificación": valor,
                "Nota": nota,
                "Comentario User": eval.comentario_User,
                "Comentario Curso": eval.comentario_curso,
                "Fecha": eval.fecha.strftime('%Y-%m-%d')
            })

    df = pd.DataFrame(datos)

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Evaluaciones')

    workbook = writer.book
    worksheet = writer.sheets['Evaluaciones']
    worksheet.set_column('A:F', 20)

    writer.close()
    output.seek(0)
    return output


