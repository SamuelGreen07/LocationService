from abc import ABC, abstractmethod


class BaseHandler(ABC):
    @abstractmethod
    def __init__(self, task_type):
        self.task_type = task_type

    @abstractmethod
    async def on_message(self, data: dict):
        raise NotImplemented
