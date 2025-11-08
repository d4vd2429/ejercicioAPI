from flask import Blueprint, request, jsonify
from config.database import SessionLocal
from models.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
	data = request.get_json() or {}
	username = data.get('username')
	email = data.get('email')
	password = data.get('password')
	if not username or not email or not password:
		return jsonify({'error': 'Faltan campos requeridos'}), 400

	db = SessionLocal()
	try:
		exists = db.query(User).filter(User.email == email).first()
		if exists:
			return jsonify({'error': 'Email ya registrado'}), 400
		user = User(username=username, email=email, password_hash=generate_password_hash(password))
		# asegurar un role por defecto para evitar errores si la columna es NOT NULL en la DB
		# Si la tabla existente tiene la columna 'role' sin default, establecer explícitamente 'user'
		user.role = 'user'
		db.add(user)
		db.commit()
		db.refresh(user)
		token = create_access_token(identity=user.id)
		return jsonify({'id': user.id, 'username': user.username, 'email': user.email, 'token': token}), 201
	finally:
		db.close()


@auth_bp.route('/login', methods=['POST'])
def login():
	data = request.get_json() or {}
	email = data.get('email')
	password = data.get('password')
	if not email or not password:
		return jsonify({'error': 'Faltan campos requeridos'}), 400

	db = SessionLocal()
	try:
		user = db.query(User).filter(User.email == email).first()
		if not user or not check_password_hash(user.password_hash, password):
			return jsonify({'error': 'Credenciales inválidas'}), 401
		token = create_access_token(identity=user.id)
		return jsonify({'token': token})
	finally:
		db.close()

