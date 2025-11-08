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

<<<<<<< HEAD
=======

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    service = _get_users_service()
    if service is None:
        return jsonify({'error': 'Servicio de usuarios no implementado'}), 501, {'Content-Type': 'application/json; charset=utf-8'}
    try:
        users = service.get_all_users()
        logger.info("Consulta de todos los usuarios")
        return jsonify([{'id': u.id, 'email': u.email, 'username': u.username, 'role': u.role} for u in users]), 200, {'Content-Type': 'application/json; charset=utf-8'}
    finally:
        try:
            service.repo.db.close()
        except Exception:
            pass


@user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    service = _get_users_service()
    if service is None:
        return jsonify({'error': 'Servicio de usuarios no implementado'}), 501, {'Content-Type': 'application/json; charset=utf-8'}
    try:
        user = service.get_user_by_id(user_id)
        if user:
            logger.info(f"Consulta de usuario por ID: {user_id}")
            return jsonify({'id': user.id, 'email': user.email, 'username': user.username, 'role': user.role}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        logger.warning(f"Usuario no encontrado: {user_id}")
        return jsonify({'error': 'Usuario no encontrado'}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    finally:
        try:
            service.repo.db.close()
        except Exception:
            pass


@user_bp.route('/registry', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    if not email or not password:
        logger.warning("Registro fallido: email o contraseña no proporcionados")
        return jsonify({'error': 'El email y la contraseña son obligatorios'}), 400, {'Content-Type': 'application/json; charset=utf-8'}

    service = _get_users_service()
    if service is None:
        return jsonify({'error': 'Servicio de usuarios no implementado'}), 501, {'Content-Type': 'application/json; charset=utf-8'}

    try:
        # validar input
        validation = service.validate_user_input(email, password)
        if validation is not None:
            status, message = validation
            logger.warning(f"Registro fallido: {message}")
            return jsonify({'error': message}), status, {'Content-Type': 'application/json; charset=utf-8'}

        # permite role si el cliente lo envía en el body (se aplicará tal cual)
        # Nota: esto permite que quien registra asigne role; si quieres
        # mantener la restricción de solo admin, vuelve a añadir la verificación.
        role = data.get('role')

        user = service.create_user(email, password, username=username)
        # si queremos soportar role en creación, actualizarlo ahora (requiere sesión)
        if role and user:
            service.repo.update_user(user.id, role=role)

        # create_user should succeed here
        logger.info(f"Usuario creado: {email}")
        return jsonify({'id': user.id, 'email': user.email, 'username': user.username}), 201, {'Content-Type': 'application/json; charset=utf-8'}
    finally:
        # intentar cerrar la sesión (el servicio usa session de SQLAlchemy)
        try:
            service.repo.db.close()
        except Exception:
            pass



@user_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Genera un nuevo access token a partir de un refresh token válido."""
    service = _get_users_service()
    if service is None:
        return jsonify({'error': 'Servicio de usuarios no implementado'}), 501, {'Content-Type': 'application/json; charset=utf-8'}
    try:
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify({'access_token': access_token}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    finally:
        try:
            service.repo.db.close()
        except Exception:
            pass



@user_bp.route('/logout', methods=['POST'])
@jwt_required(refresh=True)
def logout():
    """Revoca el refresh token actual (añade su jti a la lista de revocados)."""
    from flask_jwt_extended import get_jwt
    svc = _get_users_service()
    if svc is None:
        return jsonify({'error': 'Servicio de usuarios no implementado'}), 501, {'Content-Type': 'application/json; charset=utf-8'}
    try:
        token = get_jwt()
        jti = token.get('jti')
        # usar TokenService para revocar
        from services.token_services import TokenService
        tsvc = TokenService(svc.repo.db)
        tsvc.revoke_token(jti)
        return jsonify({'message': 'Refresh token revocado'}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    finally:
        try:
            svc.repo.db.close()
        except Exception:
            pass


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_user(user_id):
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    service = _get_users_service()
    if service is None:
        return jsonify({'error': 'Servicio de usuarios no implementado'}), 501, {'Content-Type': 'application/json; charset=utf-8'}
    try:
        user = service.update_user(user_id, username, password)
        if user:
            logger.info(f"Usuario actualizado: {user_id}")
            return jsonify({'id': user.id, 'username': user.username}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        logger.warning(f"Usuario no encontrado para actualizar: {user_id}")
        return jsonify({'error': 'Usuario no encontrado'}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    finally:
        try:
            service.repo.db.close()
        except Exception:
            pass


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_user(user_id):
    service = _get_users_service()
    if service is None:
        return jsonify({'error': 'Servicio de usuarios no implementado'}), 501, {'Content-Type': 'application/json; charset=utf-8'}
    try:
        user = service.delete_user(user_id)
        if user:
            logger.info(f"Usuario eliminado: {user_id}")
            return jsonify({'message': 'Usuario eliminado correctamente'}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        logger.warning(f"Usuario no encontrado para eliminar: {user_id}")
        return jsonify({'error': 'Usuario no encontrado'}), 404, {'Content-Type': 'application/json; charset=utf-8'}
    finally:
        try:
            service.repo.db.close()
        except Exception:
            pass
>>>>>>> 2e9fac971a1e4775ddd84eb43ed423128c842e16
