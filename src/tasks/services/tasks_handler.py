import json
import logging

from tasks.constants import TaskType
from tasks.tasks.location_handler import location_handler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TasksHandler:
    task_map = {
        TaskType.LOCATION_TASK.value: location_handler.on_message
    }

    def register_task(self, task_type, task_func):
        self.task_map[task_type] = task_func

    async def handle_message(self, message: str):
        try:
            message_data = json.loads(message)
            task_type = message_data.get("type")
            task_func = self.task_map.get(task_type)
            if task_func:
                await task_func(message_data.get('data'))
            else:
                logger.error(f"No handler registered for task type: {task_type}")
        except json.JSONDecodeError:
            logger.error("Failed to decode message")

task_handler = TasksHandler()