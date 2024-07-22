import asyncio
import base64
import json
import logging
import uuid

import aio_pika

from app import db, rabbitmq_manager
from app import app
from location.constants import TaskStatus
from location.models import Task
from location.services.location_manager import location_service_manager
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from settings import settings
from tasks.constants import TaskType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskManager:
    def __init__(self):
        self.executor = ProcessPoolExecutor(max_workers=5)

    async def calculate_distances(self, file_content):
        task_id = str(uuid.uuid4())
        async with db.get_session() as session:
            task = Task(id=task_id, status=TaskStatus.RUNNING.value)
            session.add(task)
            await session.commit()

        await self.send_task(task_id, file_content)
        return task_id

    async def send_task(self,task_id, file):
        await app.config.rabbitmq_manager.connect()
        if app.config.rabbitmq_manager.channel is None:
            logger.error("RabbitMQ channel is not initialized")
            return
        encoded_file = base64.b64encode(file).decode('utf-8')  # Кодируем файл в base64

        message_data = {
            "type": TaskType.LOCATION_TASK.value,
            "data": {
                'file':encoded_file,
                'task_id':task_id,
            }
        }
        message_body = json.dumps(message_data)
        await app.config.rabbitmq_manager.channel.default_exchange.publish(
            aio_pika.Message(body=message_body.encode()),
            routing_key=settings.QUEUE_NAME
        )
        logger.info(f"Sent task to RabbitMQ: {message_data}")
        return
    #
    # def _run_process_task(self, task_id, file_content):
    #     # Создаем новый event loop для процесса
    #     new_loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(new_loop)
    #     new_loop.run_until_complete(self._process_task(task_id, file_content))
    #     new_loop.close()

    # async def _process_task(self, task_id, file_content):
    #     await location_service_manager.process_task(task_id, file_content)

    async def get_task(self, task_id):
        return await location_service_manager.get_task(task_id)

task_manager = TaskManager()
