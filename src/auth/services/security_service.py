from passlib.context import CryptContext


class SecurityService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password: str) -> str:
        print(self.pwd_context.hash(password))
        return self.pwd_context.hash(password)

    def check_password_hash(self, hashed_password, password):
        return self.pwd_context.verify(password, hashed_password)


security_service = SecurityService()
