from flask import Blueprint, jsonify, request
from models.models import Monsters
from services.baseService import BaseService

base_service = BaseService(Monsters)
monster_bp = Blueprint('monster_bp', __name__, url_prefix='/api/monsters')

@monster_bp.route('/', methods=['GET'])
def get_monsters():
    monsters = base_service.get_all()
    return jsonify([
        {
            'id': u.idMonsters,
            'idLevel': u.idLevel,
            'name': u.name,
            'description': u.description
        }
        for u in monsters
    ]), 200

@monster_bp.route('/<int:id>', methods=['GET'])
def get_monster_by_id(id):
    monster = base_service.get_by_id(id)
    if monster:
        return jsonify({
            'id': monster.idMonsters,
            'idLevel': monster.idLevel,
            'name': monster.name,
            'description': monster.description
        }), 200
    return jsonify({'error': 'Monster not found'}), 404

@monster_bp.route('/', methods=['POST'])
def create_monster():
    data = request.json

    required_fields = ['idLevel', 'name', 'description']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_monster = base_service.create(**data)
    return jsonify({
            'id': new_monster.idMonsters,
            'idLevel': new_monster.idLevel,
            'name': new_monster.name,
            'description': new_monster.description
    }), 201

@monster_bp.route('/<int:id>', methods=['PUT'])
def update_monster(id):
    data = request.json

    updated_monster = base_service.update(id, **data)
    if updated_monster:
        return jsonify({
            'id': updated_monster.idMonsters,
            'idLevel': updated_monster.idLevel,
            'name': updated_monster.name,
            'description': updated_monster.description
        }), 200
    return jsonify({'error': 'Monster not found'}), 404

@monster_bp.route('/<int:id>', methods=['DELETE'])
def delete_monster(id):
    if base_service.delete(id):
        return jsonify({'message': 'Monster deleted successfully'})
    return jsonify({'error': 'Monster not found'}), 404