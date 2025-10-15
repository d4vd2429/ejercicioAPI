from repositories.user_repository import UserRepository
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
import re


class UsersService:
    def __init__(self, db_session: Session):
        self.repo = UserRepository(db_session)

    def authenticate_user(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

    def validate_user_input(self, email: str, password: str):
        """Return None if valid, else a tuple (status_code, message)."""
        if not email or not password:
            return 400, 'El email y la contraseña son obligatorios'
        if len(email) < 5 or len(email) > 255 or '@' not in email:
            return 400, 'El email no es válido'
        if len(password) < 6:
            return 400, 'La contraseña debe tener al menos 6 caracteres'
        if self.repo.get_by_email(email):
            return 409, 'El email ya existe'
        return None

    def get_all_users(self):
        return self.repo.get_all_users()

    def get_user_by_id(self, user_id: int):
        return self.repo.get_user_by_id(user_id)

    def create_user(self, email: str, password: str, username: str = None):
        # Validaciones básicas
        if not username or not password:
            # caller will treat None as error
            return None
        if len(username) < 3 or len(username) > 50:
            return None
        if len(password) < 6:
            return None
        # username allowed chars: letters, numbers, underscores, hyphens
        # verificar si ya existe usuario con ese email
        existing = self.repo.get_by_email(email)
        if existing:
            return None
        # hash password before saving
        pw_hash = generate_password_hash(password)
        return self.repo.create_user(email, username, pw_hash)

    def get_user_role(self, user_id: int):
        user = self.repo.get_user_by_id(user_id)
        return user.role if user else None

    def update_user(self, user_id: int, username: str = None, password: str = None):
        fields = {}
        if username:
            fields['username'] = username
        if password:
            fields['password_hash'] = generate_password_hash(password)
        return self.repo.update_user(user_id, **fields)

    def delete_user(self, user_id: int):
        return self.repo.delete_user(user_id)
