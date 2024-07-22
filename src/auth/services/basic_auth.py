from flask_httpauth import HTTPBasicAuth
from flask import request

from auth.services.security_service import security_service
from users.services.user_service import user_service

auth = HTTPBasicAuth()


@auth.verify_password
async def verify_password(email, password):
    user = await user_service.get_user_by_email(email)
    print('ffffffffffffffffffff', user)

    if not user:
        return False

    request.user = user
    return security_service.check_password_hash(user.hashed_password, password)
