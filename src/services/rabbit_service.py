import logging

import aio_pika

from tasks.services.tasks_handler import task_handler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RabbitMQManager:
    def __init__(self, config, queue_name):
        self.config = config
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            host=self.config['host'],
            port=self.config['port'],
            login=self.config['login'],
            password=self.config['password'],
            virtualhost=self.config['virtualhost']
        )

        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)
        queue = await self.channel.declare_queue(self.queue_name, durable=True)
        await queue.consume(self.on_message)

        logger.info(f"Connected to RabbitMQ and waiting for messages in '{self.queue_name}' queue.")

    async def disconnect(self):
        await self.connection.close()
        logger.info("Disconnected from RabbitMQ.")

    async def on_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            msg_body = message.body.decode()
            await task_handler.handle_message(msg_body)