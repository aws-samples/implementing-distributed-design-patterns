from abc import ABC, abstractmethod

class PointTransactionOutputPort(ABC):

    @abstractmethod
    def save(self, item):
        ...

    def get_by_id(self, id):
        ...

    def delete(self, id):
        ...

    def update(self, item):
        ...