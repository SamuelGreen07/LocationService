import argparse
import asyncio
import os


os.environ.setdefault("SETTINGS_FILE", "settings.default")

from src.settings import settings

import os

from flask import Flask

from src.services.db_wrapper import DataBaseWrapper
from urls import *
from aiohttp import web

app = Flask(__name__)

db = DataBaseWrapper()
rabbitmq_manager = None

def app_run():
    from services.rabbit_service import RabbitMQManager
    rabbitmq_manager = RabbitMQManager(settings.RABBITMQ_CONFIG, settings.QUEUE_NAME)
    # asyncio.run(rabbitmq_manager.connect())
    app.config.rabbitmq_manager = rabbitmq_manager
    app.run()
    db.init_engines_for_all_configs()

# @app.before_first_request
# def initialize():
#     db.init_engines_for_all_configs()
#     from services.rabbit_service import RabbitMQManager
#     rabbitmq_manager = RabbitMQManager(settings.RABBITMQ_CONFIG, settings.QUEUE_NAME)
#     asyncio.run(rabbitmq_manager.connect())
#     app.rabbitmq_manager = rabbitmq_manager

def run_server():
    from app import app_run
    app_run()


def run_migrations():
    os.system('alembic upgrade head')


def run_tests():
    os.system('pipenv run pytest .')


parser = argparse.ArgumentParser(description='Process some integers.')


async def init_aiohttp_app(rabbitmq_manager):
    app = web.Application()
    await rabbitmq_manager.connect()
    app.on_cleanup.append(lambda app: rabbitmq_manager.disconnect())

    # app.router.add_get('/', handler_function)

    return app


async def start_app():
    from services.rabbit_service import RabbitMQManager
    rabbitmq_manager = RabbitMQManager(settings.RABBITMQ_CONFIG, settings.QUEUE_NAME)
    app = await init_aiohttp_app(rabbitmq_manager)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    while True:
        await asyncio.sleep(3600)  # keep running


def run_aiohttp_worker():
    asyncio.run(start_app())

if __name__ == '__main__':
    FUNCTION_MAP = {
        'runserver': run_server,
        'run_aiohttp_worker': run_aiohttp_worker,
        'test': run_tests,
        'migrate': run_migrations
    }

    parser.add_argument('command', choices=FUNCTION_MAP.keys())
    args = parser.parse_args()
    func = FUNCTION_MAP[args.command]
    func()

