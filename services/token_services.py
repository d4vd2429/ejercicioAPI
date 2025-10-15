from repositories.revoked_token_repository import RevokedTokenRepository


class TokenService:
    def __init__(self, db_session):
        self.repo = RevokedTokenRepository(db_session)

    def revoke_token(self, jti: str):
        return self.repo.add(jti)

    def is_revoked(self, jti: str) -> bool:
        return self.repo.exists(jti)
