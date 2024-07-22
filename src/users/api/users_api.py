from flask import request

from marshmallow import ValidationError

from auth.services.basic_auth import auth
from users.serializers.user_serializer import CreateUserRequestSerializer, CreateUserResponseSerializer
from users.services.user_service import user_service


async def create_user_endpoint():
    try:
        user_serializer = CreateUserRequestSerializer()
        data = user_serializer.load(request.get_json())

    except ValidationError as err:
        return {'error': err.messages}, 400

    existing_user = await user_service.get_user_by_email(data['email'])
    if existing_user is not None:
        return {'error': f"User with email {data['email']} already exists."}, 400

    new_user = await user_service.create_user(data['username'], data['email'], data['password'])

    response_serializer = CreateUserResponseSerializer()
    data = response_serializer.dump(new_user)
    return data, 201


@auth.login_required
async def get_current_user_endpoint():
    response_serializer = CreateUserResponseSerializer()
    data = response_serializer.dump(request.user)
    return data, 200
