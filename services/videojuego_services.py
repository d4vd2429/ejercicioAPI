from repositories.videojuego_respository import GameRepository
from models.videojuego_model import Game
from sqlalchemy.orm import Session

"""
Librerías utilizadas:
- repositories.game_repository: Proporciona la clase GameRepository para la gestión de videojuegos en la base de datos.
- models.game_model: Define el modelo Game que representa la entidad de videojuego.
- sqlalchemy.orm.Session: Permite manejar la sesión de la base de datos para realizar operaciones transaccionales.
"""

class GameService:
    """
    Capa de servicios para la gestión de videojuegos en la tienda.
    Esta clase orquesta la lógica de negocio relacionada con los videojuegos,
    utilizando el repositorio para acceder a los datos.
    Permite mantener la lógica de negocio separada de la capa de acceso a datos.
    """

    def __init__(self, db_session: Session):
        """
        Inicializa el servicio de videojuegos con una sesión de base de datos
        y un repositorio de videojuegos.
        """
        self.repository = GameRepository(db_session)

    def listar_juegos(self):
        """
        Recupera y retorna todos los videojuegos registrados en la tienda.
        Utiliza el repositorio para obtener la lista completa de juegos.
        Es útil para mostrar catálogos o listados generales de videojuegos.
        """
        return self.repository.get_all_games()

    def obtener_juego(self, game_id: int):
        """
        Busca y retorna un videojuego específico por su identificador único (ID).
        Utiliza el repositorio para acceder al videojuego correspondiente.
        Es útil para mostrar detalles o realizar operaciones sobre un juego concreto.
        """
        return self.repository.get_game_by_id(game_id)

    def crear_juego(self, title: str, price: float, console_id: int):
        """
        Crea un nuevo videojuego con los datos proporcionados.
        Utiliza el repositorio para almacenar el nuevo juego en la base de datos.
        Es útil para registrar nuevos títulos en la tienda.
        """
        return self.repository.create_game(title, price, console_id)

    def actualizar_juego(self, game_id: int, title: str = None, price: float = None, console_id: int = None):
        """
        Actualiza la información de un videojuego existente, permitiendo modificar
        el título, precio o consola.
        Utiliza el repositorio para realizar la actualización en la base de datos.
        """
        return self.repository.update_game(game_id, title, price, console_id)

    def eliminar_juego(self, game_id: int):
        """
        Elimina un videojuego de la tienda según su identificador único (ID).
        Utiliza el repositorio para eliminar el juego de la base de datos.
        Es útil para operaciones administrativas o de mantenimiento.
        """
        return self.repository.delete_game(game_id)
