import importlib
import os


def get_settings():
    settings_file_path = os.environ.get('SETTINGS_FILE')
    if not settings_file_path:
        raise Exception('SETTINGS_FILE env variable not set')
    settings_module = importlib.import_module(settings_file_path)

    return settings_module


settings = get_settings()