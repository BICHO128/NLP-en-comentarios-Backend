# documentacion/evaluacion/auth/routes.py

from flask import Blueprint, request, jsonify
from documentacion.evaluacion.models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    email = data.get('email')
    password = data.get('password')

    # Validación de campos obligatorios
    if not email or not password:
        return jsonify({'msg': 'Correo y contraseña son obligatorios'}), 400

    user = User.query.filter_by(email=email).first()

    # Correo no registrado
    if not user:
        return jsonify({'msg': 'Credenciales incorrectas'}), 401

    # Usuario inactivo
    if not user.active:
        return jsonify({'msg': 'Usuario inactivo'}), 403

    # Contraseña incorrecta
    if not user.check_password(password):
        return jsonify({'msg': 'Credenciales incorrectas'}), 401

    # Crear token con tiempo de expiración (ya se configura globalmente)
    token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'access_token': token,
        'token_type': 'bearer',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role_id': user.role_id,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    }), 200
