# import os
# import smtplib
# from datetime import datetime
# from email.message import EmailMessage
# from documentacion.evaluacion.models import Docente

# EMAIL_REMITENTE = "david.urrutia.c@uniautonoma.edu.co"  # ← Cambia por tu correo real
# CONTRASENA = "Jdurrutia777&"              # ← Usa una app password de Gmail

# def enviar_reporte(docente_email, nombre_docente, archivo_path):
#     msg = EmailMessage()
#     msg["Subject"] = f"Reporte de Evaluación - {nombre_docente}"
#     msg["From"] = EMAIL_REMITENTE
#     msg["To"] = docente_email
#     msg.set_content(f"Hola {nombre_docente}, adjunto encontrarás tu reporte de evaluación docente.\n\nUniversidad Autónoma del Cauca.")

#     with open(archivo_path, "rb") as f:
#         contenido = f.read()
#         nombre_archivo = os.path.basename(archivo_path)
#         msg.add_attachment(contenido, maintype="application", subtype="pdf", filename=nombre_archivo)

#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
#         smtp.login(EMAIL_REMITENTE, CONTRASENA)
#         smtp.send_message(msg)

# def enviar_reportes_masivos():
#     carpeta_reportes = os.path.join("evaluacion", "reportes", "archivos_generados")
#     archivos = os.listdir(carpeta_reportes)

#     enviados = []
#     errores = []

#     for docente in Docente.query.all():
#         if docente.email:
#             nombre_archivo = f"reporte_{docente.nombre.replace(' ', '_')}.pdf"
#             archivo_path = os.path.join(carpeta_reportes, nombre_archivo)

#             if os.path.exists(archivo_path):
#                 try:
#                     enviar_reporte(docente.email, docente.nombre, archivo_path)
#                     enviados.append(docente.nombre)
#                 except Exception as e:
#                     errores.append((docente.nombre, str(e)))
#             else:
#                 errores.append((docente.nombre, "Archivo no encontrado"))

#     return {"enviados": enviados, "errores": errores}

# print("Buscando para:", Docente)
# print("Coincidencia:", Docente if Docente else "No encontrado")
# # print("Email:", Docente.email if Docente else "Sin docente")

