from flask import request, jsonify
from marshmallow import ValidationError
from auth.services.basic_auth import auth
from location.serializers.location_serializers import GetResultSerializer, TaskResultSchema
from location.tasks.location_tasks import task_manager

@auth.login_required
async def calculate_distances():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    # 'file '
    file_content = file.read()
    task_id = await task_manager.calculate_distances(file_content)

    return jsonify({'task_id': task_id, 'status': 'running'}), 202

@auth.login_required
async def get_task(task_id):

    task = await task_manager.get_task(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    result_schema = TaskResultSchema()
    task_data = result_schema.dump(task)
    return jsonify(task_data), 200