import base64

from location.services.location_manager import location_service_manager
from tasks.constants import TaskType
from tasks.tasks.base_handler import BaseHandler


class LocationHandler(BaseHandler):

    def __init__(self, task_type):
        self.task_type = task_type

    async def on_message(self, data):
        task_id = data.get("task_id")
        encoded_file_content = data.get("file")
        file_content = base64.b64decode(encoded_file_content)


        return await location_service_manager.process_task(task_id, file_content)


location_handler = LocationHandler(TaskType.LOCATION_TASK.value)