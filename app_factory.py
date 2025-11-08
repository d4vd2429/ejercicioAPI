from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

# blueprints
from controllers.videojuegos_controller import videojuegos_bp
from controllers.user_controllers import auth_bp


def create_app():
	app = Flask(__name__)
	# configuración mínima
	app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-for-testing')
	# permitir CORS para desarrollo
	CORS(app)
	JWTManager(app)

	# registrar blueprints
	app.register_blueprint(videojuegos_bp)
	app.register_blueprint(auth_bp)

	return app


if __name__ == "__main__":
	app = create_app()
	app.run(host='127.0.0.1', port=5000, debug=True)
