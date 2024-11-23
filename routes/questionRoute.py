from flask import Blueprint, jsonify, request
from models.models import Question
from services.baseService import BaseService

base_service = BaseService(Question)
question_bp = Blueprint('question_bp', __name__, url_prefix='/api/question')

@question_bp.route('/', methods=['GET'])
def get_questions():
    questions = base_service.get_all()
    return jsonify([
        {
            'id': u.idQuestion,
            'idCategory': u.idCategory,
            'content': u.content
        }
        for u in questions
    ]), 200

@question_bp.route('/<int:id>', methods=['GET'])
def get_question_by_id(id):
    questions = base_service.get_by_id(id)
    if questions:
        return jsonify({
            'id': questions.idQuestion,
            'idCategory': questions.idCategory,
            'content': questions.content
        }), 200
    return jsonify({'error': 'Question not found'}), 404

@question_bp.route('/', methods=['POST'])
def create_question():
    data = request.json

    required_fields = ['idCategory', 'content']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_question = base_service.create(**data)
    return jsonify({
            'id': new_question.idQuestion,
            'idCategory': new_question.idCategory,
            'content': new_question.content
    }), 201

@question_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    data = request.json

    update_question = base_service.update(id, **data)
    if update_question:
        return jsonify({
            'id': update_question.idQuestion,
            'idCategory': update_question.idCategory,
            'content': update_question.content
        }), 200
    return jsonify({'error': 'Question not found'}), 404

@question_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    if base_service.delete(id):
        return jsonify({'message': 'Question deleted successfully'})
    return jsonify({'error': 'Question not found'}), 404