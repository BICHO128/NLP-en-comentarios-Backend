# ⚙️ Backend - Sistema de Evaluación Docente con NLP

API RESTful construida en **Flask + SQLAlchemy + spaCy**, que permite gestionar evaluaciones docentes, procesar comentarios mediante análisis de sentimientos NLP y generar reportes automáticos en PDF y Excel.

---

## 📌 Tecnologías Utilizadas

- **Python** v3.11
- **Flask** v3.0.2
- **Flask-RESTful** v0.3.10
- **Flask-JWT-Extended** v4.6.0
- **Flask-Migrate** v4.0.5
- **Flask-CORS** v4.0.0
- **SQLAlchemy** v2.0.29
- **spaCy** v3.7.4
- **WeasyPrint** v61.3
- **openpyxl** v3.1.2
- **MySQL** v8.0.36

---

## 📌 Instalación

1. Crear entorno virtual

   ```bash
   python -m venv entorno-nlp
   ```

2. Activarlo

   ```bash
   .\entorno-nlp\Scripts\activate
   ```

3. Instalar dependencias

   ```bash
   pip install -r requirements.txt
   ```

4. Configurar base de datos en `.env`

   ```
   DATABASE_URI=mysql+pymysql://root:password@localhost/nlp_comentarios
   JWT_SECRET_KEY=mi_clave_secreta
   ```

5. Crear base de datos en MySQL Workbench.

6. Ejecutar migraciones

   ```bash
   flask db upgrade
   ```

7. Ejecutar servidor
   ```bash
   flask run
   ```

---

## 📌 Estructura de Carpetas

```
📦backend
┣  documentacion
   ┣  evaluación
      ┣ 📂admin
      ┣ 📂evaluaciones
      ┣ 📂usuarios
      ┣ 📂reportes
      ┣ 📂static
      ┣ 📂utils
      ┣ 📂templates
   ┣ 📜requirements.txt

┣ 📂migrations
┣ 📂models/sentiment
┣  entorno-nlp
┣  entorno-training
┣  hybrid_sentiment.py
┣  run.py

```

---

## 📌 Funcionalidades Principales

- API RESTful completa.
- Análisis de sentimientos con modelo spaCy (positivo, negativo, neutral).
- Registro de evaluaciones, calificaciones y comentarios.
- Generación de reportes PDF con WeasyPrint.
- Generación de reportes Excel con openpyxl.
- CRUD de estudiantes, docentes, cursos y asignación de cursos.
- Autenticación JWT y control de acceso por roles.
- Protección de rutas.
- CORS habilitado para consumo externo.
- Migraciones con Flask-Migrate.

---

## 📌 Endpoints Principales

- `POST /api/login`
- `GET /api/evaluaciones`
- `POST /api/evaluaciones`
- `GET /api/reportes/pdf/<id_docente>/<id_curso>`
- `GET /api/reportes/excel`
- CRUD: `/api/admin`, `/api/admin/crear-estudiante`, `/api/admin/listar-docentes`, `/api/admin/actualizar-curso`, `/api/admin/eliminar-estudiante`, `/api/admin/verificar-password`, `/api/admin/asignar-cursos-docente`

---

## 📌 Análisis NLP

- **Modelo:** spaCy 3.7.4
- **Categorías:** positivo, negativo, neutral
- **Pipeline:** model_matcher, tok2vec, textcat
- **Modelo cargado:** models/sentiment/model-last
- **Uso:** Clasificación automática de comentarios en tiempo real.

---

## 📌 Librerías Destacadas

- spaCy
- SQLAlchemy
- Flask-JWT-Extended
- WeasyPrint
- openpyxl

---

## 📌 Autor

**David Urrutia Cerón**  
Estudiante de Ingeniería de Software y Computación,
Corporación Universitaria Autónoma del Cauca
