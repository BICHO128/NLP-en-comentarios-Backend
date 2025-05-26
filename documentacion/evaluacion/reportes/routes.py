from datetime import datetime
from flask import Blueprint, send_file, jsonify
from io import BytesIO
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from documentacion.evaluacion.extensions import db
from documentacion.evaluacion.models import Curso, Evaluacion, Calificacion, Comentario, Criterio, User
from sqlalchemy import func
import os
from pathlib import Path
import base64
import pandas as pd
from documentacion.evaluacion.reportes.excel import generar_excel_reporte
# from documentacion.evaluacion.reportes.email_utils import enviar_reportes_masivos

# 1) FORZAMOS EL BACKEND AGG ANTES DE IMPORTAR pyplot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

reportes_bp = Blueprint("reportes", __name__)

# Constante para rol docente
DOCENTE_ROLE_ID = 2  # Ajusta según tu BD

# Ruta para generar excel para el admin, donde contiene todos los resultados, incluyendo graficas

@reportes_bp.route('/api/reportes/admin/excel', methods=['GET'])
def generar_excel_admin():
    # 1) Preparamos buffer y escritor de Excel
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    # 2) Recolectamos datos
    evaluaciones        = Evaluacion.query.all()
    filas_cal           = []  # cada calificación para pivot
    filas_sent          = []  # cada comentario para pivot
    datos_criterios     = []  # hoja "Evaluación por Criterios"
    comentarios_docente = []  # hoja "Comentarios Docente"
    comentarios_curso   = []  # hoja "Comentarios Curso"

    for ev in evaluaciones:
        usr        = ev.docente
        nombre_doc = f"{usr.first_name} {usr.last_name}"
        curso_name = ev.curso.nombre
        etiqueta   = f"{curso_name}\n{nombre_doc}"
        fecha_str  = ev.fecha.strftime("%Y-%m-%d")

        # Detalle de calificaciones
        for cal in ev.calificaciones:
            filas_cal.append({
                "Etiqueta": etiqueta,
                "Criterio": cal.criterio.descripcion,
                "Valor":    cal.valor
            })
            datos_criterios.append({
                "Docente":      nombre_doc,
                "Curso":        curso_name,
                "Criterio":     cal.criterio.descripcion,
                "Calificación": cal.valor,
                "Fecha":        fecha_str
            })

        # Detalle de comentarios
        for cm in ev.comentarios:
            filas_sent.append({
                "Etiqueta":    etiqueta,
                "Sentimiento": cm.sentimiento  # 'positivo','neutral','negativo'
            })
            fila_cm = {
                "Docente":    nombre_doc,
                "Curso":      curso_name,
                "Comentario": cm.texto,
                "Sentimiento":cm.sentimiento,
                "Fecha":      fecha_str
            }
            if cm.tipo == 'docente':
                comentarios_docente.append(fila_cm)
            else:
                comentarios_curso.append(fila_cm)

    # 3) Calculamos promedios por criterio para cada Etiqueta
    df_cal = pd.DataFrame(filas_cal)
    df_mean = (
        df_cal
        .groupby(["Etiqueta", "Criterio"])["Valor"]
        .mean()
        .reset_index()
        .round({"Valor": 1})
        .rename(columns={"Valor": "Promedio"})
    )
    df_prom_pivot = df_mean.pivot(
        index="Etiqueta",
        columns="Criterio",
        values="Promedio"
    )
    # renombrar índice para la tabla
    df_prom_pivot.index.name = "Curso con Docente"

    # 3.1) Agregar columna "promedio total"
    df_prom_pivot["nota promedio"] = df_prom_pivot.mean(axis=1).round(1)

    # 4) Pivot de conteo de sentimientos
    df_sent = pd.DataFrame(filas_sent)
    df_sent_piv = (
        df_sent
        .pivot_table(
            index="Etiqueta",
            columns="Sentimiento",
            aggfunc="size",
            fill_value=0
        )
        .reset_index()
    )
    for col in ("positivo", "neutral", "negativo"):
        if col not in df_sent_piv.columns:
            df_sent_piv[col] = 0
    # renombrar y agregar total
    df_sent_piv = df_sent_piv.rename(columns={"Etiqueta": "Curso con Docente"})
    df_sent_piv["Total"] = (
        df_sent_piv["positivo"]
        + df_sent_piv["neutral"]
        + df_sent_piv["negativo"]
    )

    # 5) Escribimos la hoja "Promedios y Graficas"
    hoja = "Promedio y Graficas"
    # a) Tabla de promedios
    df_prom_pivot.to_excel(
        writer,
        sheet_name=hoja,
        startrow=0, startcol=0,
        index_label="Curso con Docente"
    )
    # b) Tabla de sentimientos
    start_row_sent = df_prom_pivot.shape[0] + 4
    df_sent_piv.to_excel(
        writer,
        sheet_name=hoja,
        startrow=start_row_sent, startcol=0,
        index=False
    )

    workbook = writer.book
    worksheet = writer.sheets[hoja]
    chart_col = df_prom_pivot.shape[1] + 3

    # 6) Gráfica de Promedios
    # Extraemos datos de cada fila para representar en gráfica agrupada
    criterios = df_prom_pivot.columns.tolist()
    if "nota promedio" in criterios:
        criterios.remove("nota promedio")  # Excluimos la columna de promedio total
    
    # Para cada curso/docente, agruparemos por criterio
    cursos_docentes = df_prom_pivot.index.tolist()
    
    # Preparamos datos para la gráfica
    fig1, ax1 = plt.subplots(figsize=(24, 10))  # Cambiado de 16 a 20 para hacerla más ancha
    
    # Configuramos el estilo de la gráfica
    plt.style.use('default')
    plt.rcParams.update({'font.size': 16})  # Aumentamos el tamaño base de la fuente
    
    # Agrupamos por cursos/docentes
    n_criterios = len(criterios)
    # Aumentamos la separación entre grupos de barras
    x = np.arange(0, len(cursos_docentes) * 1.7, 1.7)  # Multiplicamos por 1.5 para dar más espacio entre grupos
    width = 1.2 / n_criterios  # Aumentado de 0.8 a 1.0 para dar más espacio
    
    # Colores para cada criterio
    colores = plt.cm.tab20(np.linspace(0, 1, n_criterios))
    
    # Dibujamos las barras para cada criterio
    for i, criterio in enumerate(criterios):
        valores = df_prom_pivot[criterio].values
        pos = x - 0.5 + width * (i + 0.5)  # Ajustado para centrar mejor con el nuevo espaciado
        bars = ax1.bar(pos, valores, width, label=criterio, color=colores[i])
        
        # Añadimos etiquetas de valor en cada barra
        for bar in bars:
            height = bar.get_height()
            ax1.annotate(f'{height:.1f}'.replace('.', ','),
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),  # 3 puntos de desplazamiento vertical
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=11)
    
    # Añadimos etiquetas y título
    ax1.set_title('Promedio Evalación Docente', fontsize=16, fontweight='bold')
    ax1.set_ylabel('')
    ax1.set_xlabel('')
    
    # Configuramos el eje X
    ax1.set_xticks(x)
    ax1.set_xticklabels([''] * len(cursos_docentes))  # Eliminamos etiquetas para usar nombres más abajo
    
    # Configuramos el eje Y
    ax1.set_ylim(0, 5.5)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    ax1.tick_params(axis='y', labelsize=12)  # Aumentamos tamaño de números en eje Y
    
    # Separamos la gráfica en secciones para cada curso/docente
    for i, curso_docente in enumerate(cursos_docentes):
        # Dividimos la cadena en curso y docente
        partes = curso_docente.split('\n')
        curso = partes[0]
        docente = partes[1] if len(partes) > 1 else ''
        
        # Añadimos etiquetas para cada curso y docente
        ax1.text(x[i], -0.2, curso, ha='center', va='top', fontsize=12, rotation=0)
        ax1.text(x[i], -0.35, docente, ha='center', va='top', fontsize=11, rotation=0)
    
    # Ajustamos la leyenda
    legend = ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                       ncol=n_criterios, fancybox=True, shadow=False, fontsize=11)
    
    # Ajustamos el diseño
    plt.tight_layout()
    fig1.subplots_adjust(bottom=0.25)
    
    # Guardamos la gráfica
    buf1 = BytesIO()
    fig1.savefig(buf1, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig1)
    buf1.seek(0)
    
    # Insertamos la imagen en el Excel
    worksheet.insert_image(1, chart_col, "", {
        "image_data": buf1,
        "x_scale": 0.9,
        "y_scale": 0.9
    })

    # 7) Gráfica de Sentimientos
    fig2, ax2 = plt.subplots(figsize=(20, 9))  # Cambiado de 16 a 20 para hacerla más ancha
    
    # Extraemos datos de sentimientos
    cursos_docentes = df_sent_piv['Curso con Docente'].tolist()
    
    # Configuramos el estilo de la gráfica
    plt.rcParams.update({'font.size': 16})  # Aumentamos el tamaño base de la fuente
    
    n_sentimientos = 3
    # Aumentamos la separación entre grupos de barras
    x = np.arange(0, len(cursos_docentes) * 1.5, 1.5)  # Multiplicamos por 1.5 para dar más espacio entre grupos
    width = 1.0 / n_sentimientos  # Aumentado de 0.8 a 1.0 para dar más espacio
    
    # Colores para cada sentimiento
    colores = ['green', 'yellow', 'red']
    sentimientos = ['positivo', 'neutral', 'negativo']
    
    # Calculamos el valor máximo para ajustar el eje Y
    max_value = df_sent_piv[sentimientos].max().max()
    
    # Dibujamos las barras para cada sentimiento
    for i, sentimiento in enumerate(sentimientos):
        valores = df_sent_piv[sentimiento].values
        pos = x - 0.5 + width * (i + 0.5)  # Ajustado para centrar mejor con el nuevo espaciado
        bars = ax2.bar(pos, valores, width, label=sentimiento.capitalize(), color=colores[i])
        
        # Añadimos etiquetas de valor en cada barra
        for bar in bars:
            height = bar.get_height()
            if height > 0:  # Solo mostrar etiqueta si hay valor
                ax2.annotate(f'{int(height)}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=11)
    
    # Añadimos etiquetas y título
    ax2.set_title('Cantidad de comentarios según su sentimiento', fontsize=16, fontweight='bold')
    ax2.set_ylabel('')
    ax2.set_xlabel('')
    
    # Configuramos el eje X
    ax2.set_xticks(x)
    ax2.set_xticklabels([''] * len(cursos_docentes))
    
    # Configuramos el eje Y más ajustado al contenido
    ax2.set_ylim(0, max_value * 1.1)  # Ajustamos la escala al valor máximo +10%
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    ax2.tick_params(axis='y', labelsize=12)  # Aumentamos tamaño de números en eje Y
    
    # Añadimos nombres de referencia debajo de las barras como en la primera gráfica
    for i, curso_docente in enumerate(cursos_docentes):
        # Dividimos la cadena en curso y docente
        partes = curso_docente.split('\n')
        curso = partes[0]
        docente = partes[1] if len(partes) > 1 else ''
        
        # Añadimos etiquetas debajo de las barras
        ax2.text(x[i], -max_value * 0.05, curso, ha='center', va='top', fontsize=12, rotation=0)
        ax2.text(x[i], -max_value * 0.10, docente, ha='center', va='top', fontsize=11, rotation=0)
    
    # Ajustamos la leyenda
    legend = ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                       ncol=n_sentimientos, fancybox=True, shadow=False, fontsize=11)
    
    # Ajustamos el diseño
    plt.tight_layout()
    fig2.subplots_adjust(bottom=0.2)  # Menos espacio abajo ya que hay menos elementos
    
    # Guardamos la gráfica
    buf2 = BytesIO()
    fig2.savefig(buf2, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig2)
    buf2.seek(0)
    
    # Insertamos la imagen en el Excel
    worksheet.insert_image(start_row_sent + 2, chart_col, "", {
        "image_data": buf2,
        "x_scale": 0.9,
        "y_scale": 0.9
    })

    # 8) Hojas adicionales sin gráficos
    pd.DataFrame(datos_criterios).to_excel(
        writer, sheet_name="Evaluación por Criterios", index=False
    )
    pd.DataFrame(comentarios_docente).to_excel(
        writer, sheet_name="Comentarios Docente", index=False
    )
    pd.DataFrame(comentarios_curso).to_excel(
        writer, sheet_name="Comentarios Curso", index=False
    )

    # 9) Finalizar y enviar
    writer.close()
    output.seek(0)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return send_file(
        output,
        as_attachment=True,
        download_name=f"reporte_admin_evaluaciones_{ts}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# Ruta para generar pdf por docente y curso
    
@reportes_bp.route("/api/reportes/docente/<int:docente_id>/curso/<int:curso_id>/pdf", methods=["GET"])
def generar_pdf_docente(docente_id, curso_id):
    docente_user = User.query.filter_by(id=docente_id, role_id=DOCENTE_ROLE_ID).first_or_404()
    curso = Curso.query.get_or_404(curso_id)
    # Verificar relación many-to-many
    if curso not in docente_user.cursos:
        return jsonify({'msg': "El curso no pertenece al docente"}), 400

    # Traer evaluaciones
    evs = Evaluacion.query.filter_by(docente_id=docente_id, curso_id=curso_id).all()
    if not evs:
        return jsonify({'msg': "No hay evaluaciones registradas"}), 404

    # 1. Promedio por criterio (usando tabla Calificacion)
    criterios = Criterio.query.all()
    resumen_criterios = []
    suma_promedios = 0
    for crit in criterios:
        avg = (
            db.session.query(func.avg(Calificacion.valor))
            .join(Evaluacion, Calificacion.evaluacion_id == Evaluacion.id)
            .filter(Evaluacion.docente_id == docente_id,
                    Evaluacion.curso_id == curso_id,
                    Calificacion.criterio_id == crit.id)
            .scalar() or 0
        )
        promedio = round(avg, 1)
        suma_promedios += promedio
        resumen_criterios.append({
            "criterio": crit.descripcion,
            "promedio": promedio
        })
    nota_final = round(suma_promedios / len(resumen_criterios), 1) if resumen_criterios else 0

    # 2. Comentarios y sentimientos (usando tabla Comentario)
    comentarios_doc = (
        Comentario.query.join(Evaluacion)
        .filter(Evaluacion.docente_id == docente_id,
                Evaluacion.curso_id == curso_id,
                Comentario.tipo == 'docente')
        .all()
    )
    comentarios_cu = (
        Comentario.query.join(Evaluacion)
        .filter(Evaluacion.docente_id == docente_id,
                Evaluacion.curso_id == curso_id,
                Comentario.tipo == 'curso')
        .all()
    )

    lista_comentarios = []
    for c in comentarios_doc + comentarios_cu:
        lista_comentarios.append({
            "tipo": c.tipo,
            "texto": c.texto,
            "sentimiento": c.sentimiento,
            "fecha": c.fecha.strftime("%Y-%m-%d")
        })

    # Conteo de sentimientos
    conteo_doc = {"positivo": 0, "neutral": 0, "negativo": 0}
    conteo_curso = {"positivo": 0, "neutral": 0, "negativo": 0}
    for c in comentarios_doc:
        conteo_doc[c.sentimiento] += 1
    for c in comentarios_cu:
        conteo_curso[c.sentimiento] += 1

    # Función para generar gráficos inline (base64)
    def generar_grafico(sentimientos, kind, title):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(4, 4))
        labels = ['Positivo', 'Neutral', 'Negativo']
        vals = [sentimientos['positivo'], sentimientos['neutral'], sentimientos['negativo']]
        if kind == 'pie':
            ax.pie(vals, labels=labels, autopct='%d', textprops={'fontsize':10})
        else:
            bars = ax.barh(labels, vals)
            for bar in bars:
                ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                        str(int(bar.get_width())), va='center')
        ax.set_title(title)
        buf = BytesIO()
        plt.tight_layout()
        fig.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode()

    uri_pie_doc = generar_grafico(conteo_doc, 'pie', 'Docente')
    uri_bar_doc = generar_grafico(conteo_doc, 'bar', 'Docente')
    uri_pie_cur = generar_grafico(conteo_curso, 'pie', 'Curso')
    uri_bar_cur = generar_grafico(conteo_curso, 'bar', 'Curso')
    
    # #obetener el nombre del docente
    # usuario = User.query.get_or_404(docente_user.docente_id)
    # docente_nombre = f"{usuario.first_name} {usuario.last_name}"

    # Render plantilla
    BASE_DIR = Path(__file__).parent.parent
    env = Environment(loader=FileSystemLoader(BASE_DIR / 'templates'))
    tpl = env.get_template('reporte_docente.html')
    html_str = tpl.render(
        docente=f"{docente_user.first_name} {docente_user.last_name}",
        curso=curso.nombre,
        criterios=resumen_criterios,
        nota_final=nota_final,
        comentarios=lista_comentarios,
        pie_doc=uri_pie_doc,
        bar_doc=uri_bar_doc,
        pie_cur=uri_pie_cur,
        bar_cur=uri_bar_cur
    )

    # Generar PDF
    pdf = BytesIO()
    HTML(string=html_str, base_url=str(BASE_DIR)).write_pdf(pdf)
    pdf.seek(0)
    fname = f"reporte_{docente_user.first_name}_{docente_user.last_name}_{curso.nombre.replace(' ', '_')}.pdf"
    return send_file(pdf, as_attachment=True, download_name=fname, mimetype='application/pdf')    


# @reportes_bp.route('/api/reportes/enviar-correos', methods=['GET'])
# def enviar_correos():
#     resultado = enviar_reportes_masivos()
#     return jsonify({
#         'mensaje':'Correos enviados',
#         'enviados': resultado.get('enviados',[]),
#         'errores': resultado.get('errores',[])
#     })