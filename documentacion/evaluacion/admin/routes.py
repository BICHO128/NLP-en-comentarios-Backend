# routes.py
import re
from flask import Blueprint, request, jsonify
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from documentacion.evaluacion.extensions import db
from documentacion.evaluacion.models import User, Role, Curso
from documentacion.evaluacion.schemas import CrearEstudianteSchema, CrearDocenteSchema, CrearCursoSchema
from marshmallow import ValidationError

from flask_jwt_extended import jwt_required, get_jwt_identity

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# Helper para obtener role_id
def get_role_id(role_name):
    role = Role.query.filter_by(role_name=role_name).first()
    return role.id if role else None



# ////////////////////////////////////////////////////////////////////////
# APIs PARA VERIFICAR SI ES ADMIN PARA ACCEDER A OTROS CAMPOS
# ________________________________________________________________________
@admin_bp.route('/verificar-password', methods=['POST'])
@jwt_required()  # Solo usuarios autenticados
def verificar_password():
    data = request.get_json() or {}
    print("HEADERS:", dict(request.headers))
    print("BODY RAW:", request.data)
    try:
        data = request.get_json() or {}
    except Exception as e:
        print("ERROR AL PARSEAR JSON:", e)
        return jsonify({'msg': 'Error al leer JSON'}), 400
    print("JSON recibido:", data)
    password = data.get('password')

    # Saca el usuario actual desde el token
    identity = get_jwt_identity()
    user_id = identity.get('id') if isinstance(identity, dict) else identity
    user = User.query.get(user_id)

    if not user:
        return jsonify({'msg': 'Usuario no encontrado'}), 407

    # Verifica la contraseña usando tu método de User
    if not user.check_password(password):
        return jsonify({'msg': 'Contraseña incorrecta'}), 401

    # Opcional: podrías verificar si tiene rol admin aquí
    if not user.role_id == 3:
         return jsonify({'msg': 'No eres el administrador, no tienes accedo a este campo.'}), 403
     
    print("JSON recibido:", data)
    print("password recibido:", password)
 

    return jsonify({'msg': 'Contraseña correcta'}), 200


# ////////////////////////////////////////////////////////////////////////
# APIs PARA ELIMININAR COMO TAL UN USUARIO O UN CURSO
# ________________________________________________________________________
@admin_bp.route('/eliminar-estudiante/<int:id>', methods=['DELETE'])
def eliminar_estudiante(id):
    estudiante = User.query.filter_by(id=id).first()
    if not estudiante or estudiante.role.role_name != 'estudiante':
        return jsonify({'error': 'Estudiante no encontrado'}), 404
    try:
        db.session.delete(estudiante)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar estudiante: {str(e)}'}), 500
    return jsonify({'msg': 'Estudiante eliminado correctamente'}), 200


@admin_bp.route('/eliminar-docente/<int:id>', methods=['DELETE'])
def eliminar_docente(id):
    docente = User.query.filter_by(id=id).first()
    if not docente or docente.role.role_name != 'docente':
        return jsonify({'error': 'Docente no encontrado'}), 404
    try:
        db.session.delete(docente)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar docente: {str(e)}'}), 500
    return jsonify({'msg': 'Docente eliminado correctamente'}), 200


@admin_bp.route('/eliminar-curso/<int:id>', methods=['DELETE'])
def eliminar_curso(id):
    curso = Curso.query.filter_by(id=id).first()
    if not curso:
        return jsonify({'error': 'Curso no encontrado'}), 404
    try:
        db.session.delete(curso)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar curso: {str(e)}'}), 500
    return jsonify({'msg': 'Curso eliminado correctamente'}), 200


# ////////////////////////////////////////////////////////////////////////
# APIs PARA ACTUALIZAR INFORMACIÓN
#________________________________________________________________________
@admin_bp.route('/actualizar-estudiante/<int:id>', methods=['POST', 'OPTIONS'])
def actualizar_estudiante(id):
    if request.method == 'OPTIONS':
        return '', 200
    data = request.json
    estudiante = User.query.filter_by(id=id).first()
    if not estudiante or estudiante.role.role_name != 'estudiante':
        return jsonify({'error': 'Estudiante no encontrado'}), 407

    campos_actualizables = ['username', 'email', 'first_name', 'last_name', 'active', 'password']
    hubo_cambio = False

    for campo in campos_actualizables:
        if campo in data:
            # Si es password, compara hasheando o compara el string directamente si no hay hash aún
            valor_actual = getattr(estudiante, campo, None)
            valor_nuevo = data[campo]
            if campo == "password":
                if valor_nuevo and valor_nuevo != "":
                    hubo_cambio = True
                    estudiante.password = valor_nuevo
            elif valor_nuevo is not None and str(valor_actual).strip() != str(valor_nuevo).strip():
                hubo_cambio = True
                setattr(estudiante, campo, valor_nuevo)

    if not hubo_cambio:
        return jsonify({'error': 'No has realizado ningún cambio.'}), 400

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        if 'username' in str(e).lower():
            return jsonify({'error': 'El usuario ya existe'}), 409
        if 'email' in str(e).lower():
            return jsonify({'error': 'El correo ya existe'}), 409
        return jsonify({'error': f'Error de duplicidad: {str(e)}'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar estudiante: {str(e)}'}), 500
    return jsonify({'msg': 'Estudiante actualizado correctamente'}), 200


@admin_bp.route('/actualizar-docente/<int:id>', methods=['POST', 'OPTIONS'])
def actualizar_docente(id):
    if request.method == 'OPTIONS':
        return '', 200
    data = request.json
    docente = User.query.filter_by(id=id).first()
    if not docente or docente.role.role_name != 'docente':
        return jsonify({'error': 'Docente no encontrado'}), 407

    campos_actualizables = ['username', 'email', 'first_name', 'last_name', 'active', 'password']
    hubo_cambio = False

    # Validar duplicidad ANTES de modificar el objeto, con session.no_autoflush
    #from flask_sqlalchemy import current_app
    with db.session.no_autoflush:
        if 'username' in data and data['username'].strip().lower() != docente.username.strip().lower():
            existe = User.query.filter(
                func.lower(User.username) == func.lower(data['username']),
                User.id != id
            ).first()
            if existe:
                return jsonify({'error': 'El usuario ya existe'}), 409
        if 'email' in data and data['email'].strip().lower() != docente.email.strip().lower():
            existe = User.query.filter(
                func.lower(User.email) == func.lower(data['email']),
                User.id != id
            ).first()
            if existe:
                return jsonify({'error': 'El correo ya existe'}), 409

    # Ahora sí modifica SOLO si hay cambio
    for campo in campos_actualizables:
        if campo in data:
            valor_actual = getattr(docente, campo, None)
            valor_nuevo = data[campo]
            if campo == "password":
                if valor_nuevo and valor_nuevo != "":
                    hubo_cambio = True
                    docente.password = valor_nuevo
            elif valor_nuevo is not None and str(valor_actual).strip() != str(valor_nuevo).strip():
                hubo_cambio = True
                setattr(docente, campo, valor_nuevo)

    if not hubo_cambio:
        return jsonify({'error': 'Debes cambiar al menos un campo para actualizar.'}), 400

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        if 'username' in str(e).lower():
            return jsonify({'error': 'El usuario ya existe'}), 409
        if 'email' in str(e).lower():
            return jsonify({'error': 'El correo ya existe'}), 409
        return jsonify({'error': f'Error de duplicidad: {str(e)}'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar docente: {str(e)}'}), 500
    return jsonify({'msg': 'Docente actualizado correctamente'}), 200





@admin_bp.route('/actualizar-curso/<int:id>', methods=['POST', 'OPTIONS'])
def actualizar_curso(id):
    if request.method == 'OPTIONS':
        return '', 200
    data = request.json
    curso = Curso.query.filter_by(id=id).first()
    if not curso:
        return jsonify({'error': 'Curso no encontrado'}), 407
    nuevo_nombre = data.get('nombre')

    # ✅ Validación de mínimo cambio
    if not nuevo_nombre or nuevo_nombre.strip().lower() == (curso.nombre or '').strip().lower():
        return jsonify({'error': 'No has realizado ningún cambio.'}), 400

    # Validación de duplicado (ignorando mayúsculas/minúsculas)
    existe = Curso.query.filter(
        func.lower(Curso.nombre) == func.lower(nuevo_nombre),
        Curso.id != id
    ).first()
    if existe:
        return jsonify({'error': 'El curso ya existe'}), 409

    curso.nombre = nuevo_nombre
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'El curso ya existe'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar curso: {str(e)}'}), 500
    return jsonify({'msg': 'Curso actualizado correctamente'}), 200


# ////////////////////////////////////////////////////////////////////////
# APIs PARA MOSTRAR INFORMACIÓN DE UN DOCENTE EN SI
#________________________________________________________________________
@admin_bp.route('/obtener-docente/<int:id>', methods=['GET'])
def obtener_docente(id):
    docente = User.query.filter_by(id=id).first()
    if not docente:
        return jsonify({'error': 'Docente no encontrado'}), 407
    return jsonify({
        'id': docente.id,
        'username': docente.username,
        'email': docente.email,
        'first_name': docente.first_name,
        'last_name': docente.last_name
    }), 200

@admin_bp.route('/obtener-estudiante/<int:id>', methods=['GET'])
def obtener_estudiante(id):
    estudiante = User.query.filter_by(id=id).first()
    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 407
    return jsonify({
        'id': estudiante.id,
        'username': estudiante.username,
        'email': estudiante.email,
        'first_name': estudiante.first_name,
        'last_name': estudiante.last_name
    }), 200


@admin_bp.route('/obtener-curso/<int:id>', methods=['GET'])
def obtener_curso(id):
    curso = Curso.query.filter_by(id=id).first()
    if not curso:
        return jsonify({'error': 'Curso no encontrado'}), 404
    return jsonify({
        'id': curso.id,
        'nombre': curso.nombre
    }), 200


# ////////////////////////////////////////////////////////////////////////
# APIs PARA MOSTRAR INFORMACIÓN
#________________________________________________________________________
@admin_bp.route('/listar-docentes', methods=['GET'])
def listar_docentes():
    docentes = User.query.join(Role).filter(Role.role_name == 'docente').all()
    return jsonify([
        {
            'id': docente.id,
            'username': docente.username,
            'email': docente.email,
            'first_name': docente.first_name,
            'last_name': docente.last_name
        } for docente in docentes
    ])
    
    
@admin_bp.route('/listar-estudiantes', methods=['GET'])
def listar_estudiantes():
    estudiantes = User.query.join(Role).filter(Role.role_name == 'estudiante').all()
    return jsonify([
        {
            'id': estudiante.id,
            'username': estudiante.username,
            'email': estudiante.email,
            'first_name': estudiante.first_name,
            'last_name': estudiante.last_name
        } for estudiante in estudiantes
    ])


@admin_bp.route('/listar-cursos', methods=['GET'])
def listar_cursos():
    cursos = Curso.query.all()
    return jsonify([
        {'id': curso.id, 'nombre': curso.nombre}
        for curso in cursos
    ])


@admin_bp.route('/cursos-docente/<int:docente_id>', methods=['GET'])
def cursos_por_docente(docente_id):
    docente = User.query.get(docente_id)
    if not docente or docente.role.role_name != 'docente':
        return jsonify({'error': 'Docente no encontrado'}), 407
    return jsonify([
        {'id': c.id, 'nombre': c.nombre}
        for c in docente.cursos
    ])

# ////////////////////////////////////////////////////////////////////////
# APIs PARA CREACION DE USUARIOS O CURSOS
#________________________________________________________________________
# Crear estudiante
from sqlalchemy import func  # Importar func para comparaciones case insensitive

# Expresión regular para validar contraseña segura
PASSWORD_REGEX = re.compile(
    r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};\'\\:"|,.<>\/?]).{5,}$'
)

@admin_bp.route('/crear-estudiante', methods=['POST'])
def crear_estudiante():
    schema = CrearEstudianteSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    # Validación de contraseña segura
    if not PASSWORD_REGEX.match(data['password']):
        return jsonify({
            'errors': {
                'password': 'La contraseña debe tener al menos 5 caracteres, una mayúscula, un número y un carácter especial'
            }
        }), 400
    
    # Verificación case insensitive para username y email
    if User.query.filter(func.lower(User.username) == func.lower(data['username'])).first():
        return jsonify({
            'errors': {
                'username': f'El usuario "{data["username"]}" ya está registrado'
            }
        }), 409  # Usar 409 Conflict para duplicados
    
    if User.query.filter(func.lower(User.email) == func.lower(data['email'])).first():
        return jsonify({
            'errors': {
                'email': f'El correo "{data["email"]}" ya está registrado'
            }
        }), 409

    role_id = get_role_id('estudiante')
    if not role_id:
        return jsonify({'error': 'No existe el rol estudiante'}), 500

    try:
        nuevo_usuario = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role_id=role_id
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return jsonify({
            'msg': 'Estudiante creado correctamente',
            'id': nuevo_usuario.id
        }), 201
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error de integridad en la base de datos',
            'details': str(e)
        }), 500

@admin_bp.route('/crear-curso', methods=['POST'])
def crear_curso():
    schema = CrearCursoSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    # Verificación case insensitive para nombre del curso
    if Curso.query.filter(func.lower(Curso.nombre) == func.lower(data['nombre'])).first():
        return jsonify({
            'errors': {
                'nombre': f'El curso "{data["nombre"]}" ya existe'
            }
        }), 409

    try:
        nuevo_curso = Curso(nombre=data['nombre'])
        db.session.add(nuevo_curso)
        db.session.commit()
        
        return jsonify({
            'msg': 'Curso creado correctamente',
            'curso_id': nuevo_curso.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al crear el curso',
            'details': str(e)
        }), 500

@admin_bp.route('/crear-docente', methods=['POST'])
def crear_docente():
    schema = CrearDocenteSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    # Validación de contraseña segura
    if not PASSWORD_REGEX.match(data['password']):
        return jsonify({
            'errors': {
                'password': 'La contraseña debe tener al menos 5 caracteres, una mayúscula, un número y un carácter especial'
            }
        }), 400

    # Verificación case insensitive para username y email
    if User.query.filter(func.lower(User.username) == func.lower(data['username'])).first():
        return jsonify({
            'errors': {
                'username': f'El usuario "{data["username"]}" ya está registrado'
            }
        }), 409
    
    if User.query.filter(func.lower(User.email) == func.lower(data['email'])).first():
        return jsonify({
            'errors': {
                'email': f'El correo "{data["email"]}" ya está registrado'
            }
        }), 409

    role_id = get_role_id('docente')
    if not role_id:
        return jsonify({'error': 'No existe el rol docente'}), 500

    try:
        nuevo_usuario = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role_id=role_id
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return jsonify({
            'msg': 'Docente creado correctamente',
            'id': nuevo_usuario.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al crear el docente',
            'details': str(e)
        }), 500


# ////////////////////////////////////////////////////////////////////////
# APIs PARA ASIGNAR CURSOS A UN DOCENTE
#________________________________________________________________________
@admin_bp.route('/asignar-cursos-docente', methods=['POST'])
def asignar_cursos_docente():
    from sqlalchemy.orm import joinedload
    print("==== ENTRÓ AL ENDPOINT DE ASIGNACIÓN ====")
    data = request.json
    print("data recibida:", data)

    # Cambiamos para recibir un solo docente_id en lugar de una lista
    docente_id = data.get('docente_id')  # ID único del docente
    cursos_ids = data.get('cursos_ids')  # Lista de IDs de cursos

    # Validación modificada
    if not docente_id or not cursos_ids or not isinstance(cursos_ids, list):
        print("Error: Datos incompletos o mal formateados.")
        return jsonify({'error': 'Se requiere un ID de docente y una lista de IDs de cursos'}), 400

    print(f"docente_id recibido: {docente_id}")
    print("cursos_ids recibidos:", cursos_ids)

    errores = []
    
    # Verificar si el docente existe y tiene el rol adecuado
    docente = User.query.options(joinedload(User.role)).filter(
        User.id == docente_id,
        User.role.has(role_name='docente')
    ).first()

    if not docente:
        print(f"Error: Docente con ID {docente_id} no encontrado o no es docente.")
        return jsonify({'error': 'Docente no encontrado o no tiene rol de docente'}), 404

    print(f"Docente encontrado: {docente.username} (ID: {docente_id})")

    # Limpiar cursos previos (opcional - comentar si no se desea esta funcionalidad)
    # docente.cursos = []

    cursos_asignados = []
    for curso_id in cursos_ids:
        curso = Curso.query.filter_by(id=curso_id).first()
        if curso:
            # Verificar si el curso ya está asignado para evitar duplicados
            if curso not in docente.cursos:
                docente.cursos.append(curso)
                cursos_asignados.append(curso_id)
                print(f"Curso asignado: {curso.nombre} (ID: {curso_id})")
            else:
                print(f"Info: Curso {curso_id} ya estaba asignado al docente")
                errores.append({'curso_id': curso_id, 'error': 'Curso ya estaba asignado'})
        else:
            print(f"Error: Curso con ID {curso_id} no encontrado.")
            errores.append({'curso_id': curso_id, 'error': 'Curso no encontrado'})

    try:
        db.session.commit()
        print("Asignación completada correctamente.")
    except Exception as e:
        db.session.rollback()
        print(f"Error al asignar cursos: {str(e)}")
        return jsonify({'error': f'Error al asignar cursos: {str(e)}'}), 500

    response = {
        'msg': 'Asignación de cursos completada',
        'docente_id': docente_id,
        'cursos_asignados': cursos_asignados,
        'total_cursos_asignados': len(cursos_asignados)
    }

    if errores:
        response['errores'] = errores
        return jsonify(response), 207

    return jsonify(response), 200


# ////////////////////////////////////////////////////////////////////////
# APIs PARA DESASIGNAR CURSO A UN DOCENTE
#________________________________________________________________________
@admin_bp.route('/docentes/<int:docente_id>/cursos/<int:curso_id>', methods=['DELETE'])
def desasignar_curso(docente_id, curso_id):
    from sqlalchemy.orm import joinedload
    
    print(f"==== DESASIGNANDO CURSO {curso_id} DEL DOCENTE {docente_id} ====")
    
    # Verificar si el docente existe y es docente
    docente = User.query.options(joinedload(User.role), joinedload(User.cursos)).filter(
        User.id == docente_id,
        User.role.has(role_name='docente')
    ).first()

    if not docente:
        print(f"Error: Docente con ID {docente_id} no encontrado")
        return jsonify({'error': 'Docente no encontrado o no tiene rol de docente'}), 404

    # Buscar el curso en los asignados al docente
    curso_a_remover = next((c for c in docente.cursos if c.id == curso_id), None)
    
    if not curso_a_remover:
        print(f"Error: El docente no tiene asignado el curso {curso_id}")
        return jsonify({'error': 'El curso no está asignado a este docente'}), 404

    try:
        # Remover la relación (sin eliminar el curso)
        docente.cursos.remove(curso_a_remover)
        db.session.commit()
        
        print(f"Curso {curso_id} desasignado correctamente del docente {docente_id}")
        return jsonify({
            'success': True,
            'message': f'Curso desasignado correctamente',
            'docente_id': docente_id,
            'curso_id': curso_id,
            'cursos_restantes': [c.id for c in docente.cursos]
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error al desasignar curso: {str(e)}")
        return jsonify({
            'error': 'Error al desasignar el curso',
            'details': str(e)
        }), 500




@admin_bp.route('/obtener-cursos-docente/<int:docente_id>', methods=['GET'])
def obtener_cursos_docente(docente_id):
    docente = User.query.filter_by(id=docente_id).first()
    if not docente or docente.role.role_name != 'docente':
        return jsonify({'error': 'Docente no encontrado'}), 404
    cursos = docente.cursos  # Asumiendo relación many-to-many
    return jsonify([{'id': c.id, 'nombre': c.nombre} for c in cursos])


