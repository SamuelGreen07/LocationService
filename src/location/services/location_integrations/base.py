from abc import ABC, abstractmethod

class BaseLocationService(ABC):

    @abstractmethod
    def get_address(self, latitude, longitude):
        pass

    @abstractmethod
    def get_distance(self, point1, point2):
        pass
