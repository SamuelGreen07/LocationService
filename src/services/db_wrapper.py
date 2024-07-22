from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from exceptions import ConfigurationError
from settings import settings


class DataBaseWrapper:
    def __init__(self):
        self.engines = {}

    def get_engine(self, config_name: str = None) -> AsyncEngine:
        try:
            config_name = 'DEFAULT' if config_name is None else config_name
            config = settings.DATABASE_CONFIG[config_name]
        except KeyError:
            raise KeyError(f'Database config {config_name} not found')

        if config_name in self.engines:
            return self.engines[config_name]

        self.engines[config_name] = create_async_engine(
            f"postgresql+asyncpg://{config['USER']}:{config['PASSWORD']}@{config['HOST']}:{config['PORT']}/{config['NAME']}",
            echo=True,
            # in future will be fixed
            # pool_size=config['MAX_POOL'],
            poolclass=NullPool,
            # max_overflow=0
        )

        return self.engines[config_name]

    def get_session_factory(self, engine):
        return sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    def get_session(self, config_name: str = None):
        db_engine = self.get_engine(config_name)
        return self.get_session_factory(db_engine)()

    def _merge_db_configs(self, dest_config, src_config):
        return {**dest_config, **src_config}

    def get_db_connection_string(self, migration=False):
        config: dict = settings.DATABASE_CONFIG['DEFAULT']

        if migration:
            if 'MIGRATIONS' not in config:
                raise ConfigurationError(f'database config does not have MIGRATIONS config')
            config = self._merge_db_configs(config, config['MIGRATIONS'])

        return f'{config["ENGINE"]}://{config["USER"]}:{config["PASSWORD"]}@{config["HOST"]}:{config["PORT"]}/{config["NAME"]}'

    def init_engines_for_all_configs(self):
        for config_name in settings.DATABASE_CONFIG.keys():
            self.get_engine(config_name)
