import os


locales = ['en_EN', 'en']


DATABASE_CONFIG = {
    'DEFAULT': {
        'ENGINE': 'asyncpg',
        'NAME': os.getenv('PG_DB', 'TicTacToe'),
        'USER': os.getenv('PG_USER', 'aurora'),
        'PASSWORD': os.getenv('PG_PASSWORD', 'aurorapass'),
        'HOST': os.getenv('PG_HOST', 'localhost'),
        'PORT': os.getenv('PG_PORT', 5431),
        'MAX_POOL': os.getenv('MAX_POOL', 10),
        'MIN_POOL': os.getenv('MIN_POOL', 1),
        'MIGRATIONS': {
            'ENGINE': 'postgresql'
        }
    }
}

REDIS_HOST = "127.0.0.1"
REDIS_PORT = "6379"
REDIS_DB = "0"
REDIS_CONN_STR = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"


RABBITMQ_CONFIG = {
    'host': "127.0.0.1",
    'port': 5672,
    'login': 'guest',
    'password': 'guest',
    'virtualhost': '/'
}
QUEUE_NAME = "my_queue"