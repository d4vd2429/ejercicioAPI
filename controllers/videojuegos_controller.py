
from flask import Blueprint, request, jsonify
from config.database import SessionLocal
from models.videojuego_model import Game

# Blueprint para las rutas de videojuegos
videojuegos_bp = Blueprint("videojuegos", __name__, url_prefix="/videojuegos")

# GET todos
@videojuegos_bp.route("/", methods=["GET"])
def get_videojuegos():
    db = SessionLocal()
    try:
        videojuegos = db.query(Game).all()
        return jsonify([
            {"id": v.id, "titulo": v.title, "precio": v.price, "consola_id": v.console_id}
            for v in videojuegos
        ])
    finally:
        db.close()

# GET por ID
@videojuegos_bp.route("/<int:videojuego_id>", methods=["GET"])
def get_videojuego(videojuego_id):
    db = SessionLocal()
    try:
        videojuego = db.query(Game).filter(Game.id == videojuego_id).first()
        if not videojuego:
            return jsonify({"error": "Videojuego no encontrado"}), 404
        return jsonify({"id": videojuego.id, "titulo": videojuego.title, "precio": videojuego.price, "consola_id": videojuego.console_id})
    finally:
        db.close()

# POST crear
@videojuegos_bp.route("/", methods=["POST"])
def create_videojuego():
    data = request.get_json()
    db = SessionLocal()
    try:
        nuevo = Game(title=data["titulo"], price=data["precio"], console_id=data["consola_id"])
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return jsonify({"id": nuevo.id, "titulo": nuevo.title, "precio": nuevo.price, "consola_id": nuevo.console_id}), 201
    finally:
        db.close()

# DELETE eliminar
@videojuegos_bp.route("/<int:videojuego_id>", methods=["DELETE"])
def delete_videojuego(videojuego_id):
    db = SessionLocal()
    try:
        videojuego = db.query(Game).filter(Game.id == videojuego_id).first()
        if not videojuego:
            return jsonify({"error": "Videojuego no encontrado"}), 404
        db.delete(videojuego)
        db.commit()
        return jsonify({"message": "Videojuego eliminado"})
    finally:
        db.close()

# PUT actualizar
@videojuegos_bp.route("/<int:videojuego_id>", methods=["PUT"])
def update_videojuego(videojuego_id):
    data = request.get_json()
    db = SessionLocal()
    try:
        videojuego = db.query(Game).filter(Game.id == videojuego_id).first()
        if not videojuego:
            return jsonify({"error": "Videojuego no encontrado"}), 404
        videojuego.title = data.get("titulo", videojuego.title)
        videojuego.price = data.get("precio", videojuego.price)
        videojuego.console_id = data.get("consola_id", videojuego.console_id)
        db.commit()
        db.refresh(videojuego)
        return jsonify({
            "id": videojuego.id,
            "titulo": videojuego.title,
            "precio": videojuego.price,
            "consola_id": videojuego.console_id
        })
    finally:
        db.close()
