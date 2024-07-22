from sqlalchemy import select

from app import db
from auth.services.basic_auth import security_service
from users.models import User


class UserService:

    async def create_user(self, username, email, password):
        async with db.get_session() as session:
            new_user = User(
                username=username,
                email=email,
                hashed_password=security_service.get_password_hash(password)
            )
            session.add(new_user)
            await session.commit()
        return new_user

    async def get_user_by_email(self, email):
        async with db.get_session() as session:

            query = select(User).where(User.email == email)
            result = await session.execute(query)

            user = result.scalars().first()
            session.close()
        return user



user_service = UserService()
