import bcrypt
from flask import Blueprint, jsonify, request
from models.models import User
from services.baseService import BaseService

base_service = BaseService(User)
user_bp = Blueprint('user_bp', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
def get_users():
    users = base_service.get_all()
    return jsonify([
        {
            'id': u.idUser,
            'idCard': u.idCard,
            'names': u.names,
            'surnames': u.surnames,
            'email': u.email,
            'password': u.password, # Se puede dejar de mostrar por seguridad
            'score': u.score
        }
        for u in users
    ]), 200

@user_bp.route('/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = base_service.get_by_id(id)
    if user:
        return jsonify({
            'id': user.idUser,
            'idCard': user.idCard,
            'names': user.names,
            'surnames': user.surnames,
            'email': user.email,
            'password': user.password, # Se puede dejar de mostrar por seguridad
            'score': user.score
        }), 200
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.json

    required_fields = ['idCard', 'names', 'surnames', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    password = data['password'].encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    data['password'] = hashed_password.decode('utf-8')

    data['score'] = data.get('score', 0)

    new_user = base_service.create(**data)
    return jsonify({
        'id': new_user.idUser,
        'idCard': new_user.idCard,
        'names': new_user.names,
        'surnames': new_user.surnames,
        'email': new_user.email,
        'password': new_user.password, # Se puede dejar de mostrar por seguridad
        'score': new_user.score
    }), 201

@user_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json

    updated_user = base_service.update(id, **data)
    if updated_user:
        return jsonify({
            'id': updated_user.idUser,
            'idCard': updated_user.idCard,
            'names': updated_user.names,
            'surnames': updated_user.surnames,
            'email': updated_user.email,
            'password': updated_user.password, # Se puede dejar de mostrar por seguridad
            'score': updated_user.score
        }), 200
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    if base_service.delete(id):
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'error': 'User not found'}), 404

# Ruta para validar credenciales de inicio de sesión
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = base_service.get_by_email(email)
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401

    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'message': 'Login successful', 'id': user.idUser}), 200
    return jsonify({'error': 'Invalid email or password'}), 401