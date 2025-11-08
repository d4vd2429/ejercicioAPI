from sqlalchemy import Column, Integer, String, text
from models.videojuego_model import Base


class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True, index=True)
	username = Column(String(150), nullable=False)
	email = Column(String(255), nullable=False, unique=True)
	password_hash = Column(String(255), nullable=False)
	# agregar role por compatibilidad con la DB existente; establecer default a 'user'
	role = Column(String(50), nullable=False, server_default=text("'user'"))

