
from flask import Blueprint, request, jsonify
from services.videojuego_services import GameService
game_bp =Blueprint('game_bp',__name__)


# Importar la sesión de la base de datos
from config.database import get_db_session

game_bp = Blueprint('game_bp', __name__)

# Instancia global de servicio (en producción usar contexto de app o request)
service = GameService(get_db_session())


@game_bp.route('/games', methods=['GET'])
def get_games():
    """
    GET /games
    Recupera y retorna todos los videojuegos registrados en la tienda.
    """
    games = service.listar_juegos()
    return jsonify([{'id': g.id, 'title': g.title, 'price': g.price} for g in games]), 200


@game_bp.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    """
    GET /games/<game_id>
    Recupera la información de un videojuego específico por su ID.
    """
    game = service.obtener_juego(game_id)
    if game:
        return jsonify({'id': game.id, 'title': game.title, 'price': game.price}), 200
    return jsonify({'error': 'Videojuego no encontrado'}), 404


@game_bp.route('/games', methods=['POST'])
def create_game():
    """
    POST /games
    Crea un nuevo videojuego en la tienda.
    Parámetros esperados (JSON):
        title (str): Título del videojuego.
        price (float): Precio del videojuego.
    """
    data = request.get_json()
    title = data.get('title')
    price = data.get('price')

    if not title or price is None:
        return jsonify({'error': 'El título y el precio son obligatorios'}), 400

    game = service.crear_juego(title, price)
    return jsonify({'id': game.id, 'title': game.title, 'price': game.price}), 201


@game_bp.route('/games/<int:game_id>', methods=['PUT'])
def update_game(game_id):
    """
    PUT /games/<game_id>
    Actualiza la información de un videojuego existente.
    """
    data = request.get_json()
    title = data.get('title')
    price = data.get('price')

    game = service.actualizar_juego(game_id, title, price)
    if game:
        return jsonify({'id': game.id, 'title': game.title, 'price': game.price}), 200
    return jsonify({'error': 'Videojuego no encontrado'}), 404


@game_bp.route('/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    """
    DELETE /games/<game_id>
    Elimina un videojuego específico por su ID.
    """
    game = service.eliminar_juego(game_id)
    if game:
        return jsonify({'message': 'Videojuego eliminado'}), 200
    return jsonify({'error': 'Videojuego no encontrado'}), 404
