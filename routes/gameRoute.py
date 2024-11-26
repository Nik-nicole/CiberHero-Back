from flask import Blueprint, jsonify, request
from models.models import Game, User, Monsters
from services.baseService import BaseService
from extensions import db

base_service = BaseService(Game)
game_bp = Blueprint('game_bp', __name__, url_prefix='/api/games')

@game_bp.route('/', methods=['GET'])
def get_games():
    games = base_service.get_all()
    return jsonify([
        {
            'id': u.idGame,
            'idUser': u.idUser,
            'startDate': u.startDate,
            'endDate': u.endDate,
            'finalScore': u.finalScore
        }
        for u in games
    ]), 200

@game_bp.route('/<int:id>', methods=['GET'])
def get_game_by_id(id):
    game = base_service.get_by_id(id)
    if game:
        return jsonify({
            'id': game.idGame,
            'idUser': game.idUser,
            'startDate': game.startDate,
            'endDate': game.endDate,
            'finalScore': game.finalScore
        }), 200
    return jsonify({'error': 'Game not found'}), 404

@game_bp.route('/', methods=['POST'])
def create_game():
    data = request.json

    required_fields = ['idUser', 'startDate', 'endDate', 'finalScore']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_game = base_service.create(**data)
    return jsonify({
        'id': new_game.idGame,
        'idUser': new_game.idUser,
        'startDate': new_game.startDate,
        'endDate': new_game.endDate,
        'finalScore': new_game.finalScore
    }), 201

@game_bp.route('/<int:id>', methods=['PUT'])
def update_game(id):
    data = request.json

    updated_game = base_service.update(id, **data)
    if updated_game:
        return jsonify({
            'id': updated_game.idGame,
            'idUser': updated_game.idUser,
            'startDate': updated_game.startDate,
            'endDate': updated_game.endDate,
            'finalScore': updated_game.finalScore
        }), 200
    return jsonify({'error': 'Game not found'}), 404

@game_bp.route('/<int:id>', methods=['DELETE'])
def delete_game(id):
    if base_service.delete(id):
        return jsonify({'message': 'Game deleted successfully'})
    return jsonify({'error': 'Game not found'}), 404