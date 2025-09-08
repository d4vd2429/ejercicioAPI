from models.videojuego_model import Game, Console
from sqlalchemy.orm import Session

class GameRepository:
    """
    Repositorio para la gestión de videojuegos en la base de datos.
    Proporciona métodos para crear, consultar, actualizar y eliminar videojuegos,
    así como para gestionar la relación con las consolas.
    """

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_games(self):
        """
        Recupera todos los videojuegos almacenados en la base de datos.
        Retorna una lista de objetos Game.
        """
        return self.db.query(Game).all()

    def get_game_by_id(self, game_id: int):
        """
        Busca y retorna un videojuego específico según su ID.
        Devuelve la instancia de Game si existe, o None si no se encuentra.
        """
        return self.db.query(Game).filter(Game.id == game_id).first()

    def create_game(self, title: str, price: float, console_id: int):
        """
        Crea y almacena un nuevo videojuego en la base de datos.
        Parámetros:
            title (str): Título del videojuego.
            price (float): Precio del videojuego.
            console_id (int): ID de la consola a la que pertenece.
        Retorna la instancia de Game creada.
        """
        new_game = Game(title=title, price=price, console_id=console_id)
        self.db.add(new_game)
        self.db.commit()
        self.db.refresh(new_game)
        return new_game

    def update_game(self, game_id: int, title: str = None, price: float = None, console_id: int = None):
        """
        Actualiza los datos de un videojuego existente en la base de datos.
        Permite modificar el título, precio o consola de un videojuego.
        Retorna la instancia actualizada o None si no existe.
        """
        game = self.get_game_by_id(game_id)
        if game:
            if title:
                game.title = title
            if price is not None:
                game.price = price
            if console_id:
                game.console_id = console_id
            self.db.commit()
            self.db.refresh(game)
        return game

    def delete_game(self, game_id: int):
        """
        Elimina un videojuego de la base de datos según su ID.
        Retorna la instancia eliminada o None si no existe.
        """
        game = self.get_game_by_id(game_id)
        if game:
            self.db.delete(game)
            self.db.commit()
        return game
