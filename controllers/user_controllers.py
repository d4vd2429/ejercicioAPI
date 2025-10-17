import logging
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token, get_jwt_identity
from utils.auth_utils import role_required
from flask_jwt_extended.exceptions import NoAuthorizationError

from config.database import get_db_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Helper to obtain the UsersService if it exists. If not, controller will
# return 501 responses with a helpful message so the app doesn't crash at import.
def _get_users_service():
    try:
        from services.users_services import UsersService
    except Exception as e:
        logger.warning("UsersService no disponible: %s", e)
        return None
    # create a short-lived DB session per request
    return UsersService(get_db_session())


user_bp = Blueprint('users', __name__)


def register_jwt_error_handlers(app):
    @app.errorhandler(NoAuthorizationError)
    def handle_no_auth_error(e):
        logger.warning("Intento de acceso sin autenticación JWT")
        return jsonify({'error': 'No autenticado. Debe enviar un token JWT valido en el header Authorization.'}), 401, {'Content-Type': 'application/json; charset=utf-8'}


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        logger.warning("Login fallido: email o contrasena no proporcionados")
        return jsonify({'error': 'El email y la contrasena son obligatorios'}), 400, {'Content-Type': 'application/json; charset=utf-8'}

    service = _get_users_service()
    if service is None:
        return jsonify({'error': 'Servicio de usuarios no implementado'}), 501, {'Content-Type': 'application/json; charset=utf-8'}
    try:
        user = service.authenticate_user(email, password)
        if user:
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            logger.info(f"Usuario autenticado: {email}")
            return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        logger.warning(f"Login fallido para email: {email}")
        return jsonify({'error': 'Credenciales invalidas'}), 401, {'Content-Type': 'application/json; charset=utf-8'}
    finally:
        try:
            service.repo.db.close()
        except Exception:
            pass


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
