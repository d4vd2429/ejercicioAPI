from flask import Flask
from config.database import Base, engine, get_db_session
from controllers.videojuegos_controller import videojuegos_bp
from controllers.user_controllers import user_bp, register_jwt_error_handlers
from flask_jwt_extended import JWTManager
import os


def create_app(test_config: dict = None):
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret')
    if test_config:
        app.config.update(test_config)
    jwt = JWTManager(app)
    # register token blocklist check
    from services.token_services import TokenService

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload.get('jti')
        svc = TokenService(get_db_session())
        try:
            return svc.is_revoked(jti)
        finally:
            try:
                svc.repo.db.close()
            except Exception:
                pass

    # create tables
    Base.metadata.create_all(bind=engine)

    app.register_blueprint(videojuegos_bp)
    app.register_blueprint(user_bp)
    register_jwt_error_handlers(app)

    return app
