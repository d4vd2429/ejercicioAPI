from models.revoked_token_model import RevokedToken


class RevokedTokenRepository:
    def __init__(self, db_session):
        self.db = db_session

    def add(self, jti: str):
        rt = RevokedToken(jti=jti)
        self.db.add(rt)
        self.db.commit()
        return rt

    def exists(self, jti: str) -> bool:
        return self.db.query(RevokedToken).filter(RevokedToken.jti == jti).first() is not None
