from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify


def role_required(role_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            if not identity:
                return jsonify({'error': 'No autenticado'}), 401
            # Lazy import to avoid circular
            from services.users_services import UsersService
            from config.database import get_db_session
            svc = UsersService(get_db_session())
            try:
                user_role = svc.get_user_role(int(identity))
                if user_role != role_name:
                    return jsonify({'error': 'Permisos insuficientes'}), 403
                return fn(*args, **kwargs)
            finally:
                try:
                    svc.repo.db.close()
                except Exception:
                    pass
        return wrapper
    return decorator
