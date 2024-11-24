from flask import Blueprint, jsonify, request
from models.models import GameHasMonsters
from services.baseService import BaseService

base_service = BaseService(GameHasMonsters)
gameHasMonsters_bp = Blueprint('gameHasMonsters_bp', __name__, url_prefix='/api/gameHasMonsters')

@gameHasMonsters_bp.route('/', methods=['GET'])
def get_gameHasMonsters():
    gameHasMonsters = base_service.get_all()
    return jsonify([
        {
            'id': u.idGameHasMonsters,
            'idGame': u.idGame,
            'idUser': u.idUser,
            'idMonsters': u.idMonsters,
            'idLevel': u.idLevel
        }
        for u in gameHasMonsters
    ]), 200

@gameHasMonsters_bp.route('/<int:id>', methods=['GET'])
def get_gameHasMonsters_by_id(id):
    gameHasMonsters = base_service.get_by_id(id)
    if gameHasMonsters:
        return jsonify({
            'id': gameHasMonsters.idGameHasMonsters,
            'idGame': gameHasMonsters.idGame,
            'idUser': gameHasMonsters.idUser,
            'idMonsters': gameHasMonsters.idMonsters,
            'idLevel': gameHasMonsters.idLevel
        }), 200
    return jsonify({'error': 'Game Has Monsters not found'}), 404

@gameHasMonsters_bp.route('/', methods=['POST'])
def create_gameHasMonsters():
    data = request.json

    required_fields = ['idGame', 'idUser', 'idMonsters', 'idLevel']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_gameHasMonsters = base_service.create(**data)
    return jsonify({
            'id': new_gameHasMonsters.idGameHasMonsters,
            'idGame': new_gameHasMonsters.idGame,
            'idUser': new_gameHasMonsters.idUser,
            'idMonsters': new_gameHasMonsters.idMonsters,
            'idLevel': new_gameHasMonsters.idLevel
    }), 201

@gameHasMonsters_bp.route('/<int:id>', methods=['PUT'])
def update_gameHasMonsters(id):
    data = request.json

    updated_gameHasMonsters = base_service.update(id, **data)
    if updated_gameHasMonsters:
        return jsonify({
            'id': updated_gameHasMonsters.idGameHasMonsters,
            'idGame': updated_gameHasMonsters.idGame,
            'idUser': updated_gameHasMonsters.idUser,
            'idMonsters': updated_gameHasMonsters.idMonsters,
            'idLevel': updated_gameHasMonsters.idLevel
        }), 200
    return jsonify({'error': 'Game Has Monsters not found'}), 404

@gameHasMonsters_bp.route('/<int:id>', methods=['DELETE'])
def delete_gameHasMonsters(id):
    if base_service.delete(id):
        return jsonify({'message': 'Game Has Monsters deleted successfully'})
    return jsonify({'error': 'Game Has Monsters not found'}), 404