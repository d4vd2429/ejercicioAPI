from flask import Flask
from controllers.videojueos_controller import game_bp  # Importamos el blueprint de videojuegos

app = Flask(__name__)

# Registrar el blueprint de videojuegos
app.register_blueprint(game_bp, url_prefix="/games")

if __name__ == "__main__":
    app.run(debug=True)
