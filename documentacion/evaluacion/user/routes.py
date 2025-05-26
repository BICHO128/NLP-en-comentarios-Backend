from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
from documentacion.evaluacion.models import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('nombre_usuario')
    password = data.get('password')

    user = User.query.filter_by(nombre_usuario=username).first()

    if user and check_password_hash(user.password, password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.now() + timedelta(hours=2)
        }, 'secreto_jwt_super_seguro', algorithm='HS256')

        return jsonify({
            'token': token,
            'usuario': {
                'id': user.id,
                'username': user.nombre_usuario,
                'first_name': user.nombres,
                'last_name': user.apellidos,
                'email': user.email,
                'is_admin': user.es_admin
            }
        }), 200

    return jsonify({'error': 'Credenciales inválidas'}), 401
