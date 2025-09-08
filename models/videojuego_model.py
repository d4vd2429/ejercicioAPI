from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

"""
La clase Console representa una consola de videojuegos dentro del sistema.
Cada consola puede estar asociada a múltiples videojuegos (relación uno a muchos).
Esta clase está mapeada a la tabla 'consoles' en la base de datos.
"""
class Console(Base):
    __tablename__ = 'consoles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    # Relación: una consola puede tener varios videojuegos
    games = relationship('Game', back_populates='console', cascade='all, delete-orphan')


"""
La clase Game representa un videojuego en la tienda.
Cada videojuego pertenece a una consola específica (relación muchos a uno).
Esta clase está mapeada a la tabla 'games' en la base de datos.
"""
class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)

    # Relación con la consola (clave foránea)
    console_id = Column(Integer, ForeignKey('consoles.id'))
    console = relationship('Console', back_populates='games')
