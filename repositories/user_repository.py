from models.user_model import User
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_users(self):
        return self.db.query(User).all()

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, email: str, username: str, password_hash: str):
        user = User(email=email, username=username, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user_id: int, **fields):
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        for k, v in fields.items():
            setattr(user, k, v)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        self.db.delete(user)
        self.db.commit()
        return user
