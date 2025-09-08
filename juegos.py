from flask import Flask
from config.database import Base, engine
from controllers.videojuegos_controller import videojuegos_bp

app = Flask(__name__)

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Registrar las rutas
app.register_blueprint(videojuegos_bp)

if __name__ == "__main__":
    app.run(debug=True)
