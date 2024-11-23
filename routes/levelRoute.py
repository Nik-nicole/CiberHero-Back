from flask import Blueprint, jsonify, request
from models.models import Level
from services.baseService import BaseService

base_service = BaseService(Level)
level_bp = Blueprint('level_bp', __name__, url_prefix='/api/levels')

@level_bp.route('/', methods=['GET'])
def get_levels():
    levels = base_service.get_all()
    return jsonify([
        {
            'id': u.idLevel,
            'difficulty': u.difficulty
        }
        for u in levels
    ]), 200

@level_bp.route('/<int:id>', methods=['GET'])
def get_level_by_id(id):
    level = base_service.get_by_id(id)
    if level:
        return jsonify({
            'id': level.idLevel,
            'difficulty': level.difficulty
        }), 200
    return jsonify({'error': 'Level not found'}), 404

@level_bp.route('/', methods=['POST'])
def create_level():
    data = request.json

    required_fields = ['difficulty']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_level = base_service.create(**data)
    return jsonify({
            'id': new_level.idLevel,
            'difficulty': new_level.difficulty
    }), 201

@level_bp.route('/<int:id>', methods=['PUT'])
def update_level(id):
    data = request.json

    updated_level = base_service.update(id, **data)
    if updated_level:
        return jsonify({
            'id': updated_level.idLevel,
            'difficulty': updated_level.difficulty
        }), 200
    return jsonify({'error': 'Level not found'}), 404

@level_bp.route('/<int:id>', methods=['DELETE'])
def delete_level(id):
    if base_service.delete(id):
        return jsonify({'message': 'Level deleted successfully'})
    return jsonify({'error': 'Level not found'}), 404