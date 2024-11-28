from flask import Blueprint, jsonify, request
from models.models import Question
from services.baseService import BaseService
from transformers import pipeline
import os
import random

# Configuración del pipeline de Hugging Face
api_key = os.getenv("API_KEY")  # Asegúrate de configurar esta variable de entorno correctamente
if not api_key:
    raise ValueError("La API key de Hugging Face no está configurada.")

# Usando un modelo preentrenado que soporte parafraseo específico
nlp_pipeline = pipeline("text2text-generation", model="t5-base")  # Usamos el modelo T5, que es comúnmente utilizado para parafrasear

# Base service y blueprint
base_service = BaseService(Question)
question_bp = Blueprint("question_bp", __name__, url_prefix="/api/question")

# Lista de prompts de parafraseo
prompts = [
    "Reformula la siguiente pregunta utilizando sinónimos y reorganizando la estructura gramatical, pero asegúrate de que siga siendo una pregunta válida con el mismo significado: {original_content}",
    "Reformula esta pregunta de manera que conserve el mismo propósito y significado, pero cambia el estilo y las palabras usadas: {original_content}",
    "Reescribe esta pregunta de manera que transmita exactamente la misma intención, utilizando una estructura y palabras distintas: {original_content}",
    "Crea una versión alternativa de esta pregunta que mantenga el mismo sentido y propósito, utilizando sinónimos y una posible reestructuración: {original_content}"
]
# CRUD Básico de preguntas
@question_bp.route('/', methods=['GET'])
def get_questions():
    questions = base_service.get_all()
    return jsonify([{
        'id': u.idQuestion,
        'idCategory': u.idCategory,
        'content': u.content
    } for u in questions]), 200

@question_bp.route('/<int:id>', methods=['GET'])
def get_question_by_id(id):
    question = base_service.get_by_id(id)
    if question:
        return jsonify({
            'id': question.idQuestion,
            'idCategory': question.idCategory,
            'content': question.content
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


# Endpoint AI: transformar preguntas
@question_bp.route("/ai/<int:id>", methods=["GET"])
def transform_question_mbart(id):
    question = base_service.get_by_id(id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    original_content = question.content
    
    # Seleccionar un prompt aleatorio de la lista
    selected_prompt = random.choice(prompts).format(original_content=original_content)

    # Generar la reformulación utilizando el modelo T5 (más adecuado para este caso)
    paraphrased_text = nlp_pipeline(selected_prompt, max_length=100, num_return_sequences=1)

    if paraphrased_text:
        # Obtener el contenido reformulado
        transformed_content = paraphrased_text[0]['generated_text'].strip()
        return jsonify({
            "original_content": original_content,
            "paraphrased_content": transformed_content
        }), 200

    return jsonify({"error": "No se pudo reformular la pregunta adecuadamente"}), 500