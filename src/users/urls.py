from flask import Blueprint

from users.api.users_api import create_user_endpoint, get_current_user_endpoint

user_blueprint = Blueprint('user_blueprint', __name__)

user_blueprint.add_url_rule('/create_user/', 'create_user', create_user_endpoint, methods=['POST'])
user_blueprint.add_url_rule('/user/', 'get_current_user_endpoint', get_current_user_endpoint, methods=['GET'])
