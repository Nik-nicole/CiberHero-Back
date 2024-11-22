from flask import Blueprint, jsonify, request
from models.models import Answer
from services.baseService import BaseService

base_service = BaseService(Answer)
answer_bp = Blueprint('answer_bp', __name__, url_prefix='/api/answer')

@answer_bp.route('/', methods=['GET'])
def get_answer():
    answer = base_service.get_all()
    return jsonify([
        {
            'id': u.idAnswer,
            'idQuestion': u.idQuestion,
            'answer': u.answer,
            'isCorrect': u.isCorrect
        }
        for u in answer
    ]), 200

@answer_bp.route('/<int:id>', methods=['GET'])
def get_answer_by_id(id):
    answer = base_service.get_by_id(id)
    if answer:
        return jsonify({
            'id': answer.idAnswer,
            'idQuestion': answer.idQuestion,
            'answer': answer.answer,
            'isCorrect': answer.isCorrect
        }), 200
    return jsonify({'error': 'Answer not found'}), 404

@answer_bp.route('/', methods=['POST'])
def create_answer():
    data = request.json

    required_fields = ['idAnswer', 'idQuestion', 'answer', 'isCorrect']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_game = base_service.create(**data)
    return jsonify({
            'id': new_game.idAnswer,
            'idQuestion': new_game.idQuestion,
            'answer': new_game.answer,
            'isCorrect': new_game.isCorrect
    }), 201

@answer_bp.route('/<int:id>', methods=['PUT'])
def update_answer(id):
    data = request.json

    updated_answer = base_service.update(id, **data)
    if updated_answer:
        return jsonify({
            'id': updated_answer.idAnswer,
            'idUser': updated_answer.idQuestion,
            'startDate': updated_answer.answer,
            'endDate': updated_answer.isCorrect
        }), 200
    return jsonify({'error': 'Answer not found'}), 404

@answer_bp.route('/<int:id>', methods=['DELETE'])
def delete_answer(id):
    if base_service.delete(id):
        return jsonify({'message': 'Answer deleted successfully'})
    return jsonify({'error': 'Answer not found'}), 404