from flask import Blueprint, jsonify, request
from models.models import Category
from services.baseService import BaseService

base_service = BaseService(Category)
category_bp = Blueprint('category_bp', __name__, url_prefix='/api/categories')

@category_bp.route('/', methods=['GET'])
def get_categories():
    categories = base_service.get_all()
    return jsonify([
        {
            'id': u.idCategory,
            'idMonster': u.idMonster,
            'category': u.category
        }
        for u in categories
    ]), 200

@category_bp.route('/<int:id>', methods=['GET'])
def get_category_by_id(id):
    category = base_service.get_by_id(id)
    if category:
        return jsonify({
            'id': category.idCategory,
            'idMonster': category.idMonster,
            'category': category.category
        }), 200
    return jsonify({'error': 'Category not found'}), 404

@category_bp.route('/', methods=['POST'])
def create_category():
    data = request.json

    required_fields = ['idMonsters', 'category']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_category = base_service.create(**data)
    return jsonify({
            'id': new_category.idCategory,
            'idMonsters': new_category.idMonsters,
            'category': new_category.category
    }), 201

@category_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.json

    update_category = base_service.update(id, **data)
    if update_category:
        return jsonify({
            'id': update_category.idCategory,
            'idMonster': update_category.idMonster,
            'category': update_category.category
        }), 200
    return jsonify({'error': 'Category not found'}), 404

@category_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    if base_service.delete(id):
        return jsonify({'message': 'Category deleted successfully'})
    return jsonify({'error': 'Category not found'}), 404