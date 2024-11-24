from flask import Blueprint, jsonify, request
from models.models import GameHasLevel
from services.baseService import BaseService

base_service = BaseService(GameHasLevel)
gameHasLevels_bp = Blueprint('gameHasLevels_bp', __name__, url_prefix='/api/gameHasLevels')

@gameHasLevels_bp.route('/', methods=['GET'])
def get_gameHasLevels():
    gameHasLevels = base_service.get_all()
    return jsonify([
        {
            'id': u.idGameHasLevels,
            'idGame': u.idGame,
            'idUser': u.idUser,
            'idLevel': u.idLevel
        }
        for u in gameHasLevels
    ]), 200

@gameHasLevels_bp.route('/<int:id>', methods=['GET'])
def get_gameHasLevels_by_id(id):
    gameHasLevels = base_service.get_by_id(id)
    if gameHasLevels:
        return jsonify({
            'id': gameHasLevels.idGameHasLevels,
            'idGame': gameHasLevels.idGame,
            'idUser': gameHasLevels.idUser,
            'idLevel': gameHasLevels.idLevel
        }), 200
    return jsonify({'error': 'Game Has Levels not found'}), 404

@gameHasLevels_bp.route('/', methods=['POST'])
def create_gameHasLevels():
    data = request.json

    required_fields = ['idGame', 'idUser', 'idLevel']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_gameHasLevels = base_service.create(**data)
    return jsonify({
            'id': new_gameHasLevels.idGameHasMonsters,
            'idGame': new_gameHasLevels.idGame,
            'idUser': new_gameHasLevels.idUser,
            'idLevel': new_gameHasLevels.idLevel
    }), 201

@gameHasLevels_bp.route('/<int:id>', methods=['PUT'])
def update_gameHasLevels(id):
    data = request.json

    update_gameHasLevels = base_service.update(id, **data)
    if update_gameHasLevels:
        return jsonify({
            'id': update_gameHasLevels.idGameHasMonsters,
            'idGame': update_gameHasLevels.idGame,
            'idUser': update_gameHasLevels.idUser,
            'idLevel': update_gameHasLevels.idLevel
        }), 200
    return jsonify({'error': 'Game Has Levels not found'}), 404

@gameHasLevels_bp.route('/<int:id>', methods=['DELETE'])
def delete_gameHasLevels(id):
    if base_service.delete(id):
        return jsonify({'message': 'Game Has Levels deleted successfully'})
    return jsonify({'error': 'Game Has Levels not found'}), 404