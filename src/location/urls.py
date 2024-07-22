from location.api.location_api import calculate_distances, get_task

from flask import Blueprint

location_blueprint = Blueprint('location_blueprint', __name__)

location_blueprint.add_url_rule('/calculate_distances/', 'calculate_distances', calculate_distances, methods=['POST'])
location_blueprint.add_url_rule('/distances_task/<task_id>/', 'get_task', get_task, methods=['GET'])
