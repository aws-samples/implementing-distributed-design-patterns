from abc import ABC, abstractmethod
from datetime import date

class PointBalanceOutputPort(ABC):

    @abstractmethod
    def save(self, item):
        ...

    @abstractmethod
    def update_account_balance_by_date(self, item):
        ...

    @abstractmethod
    def deduct_account_balance(self, item):
        ...

    @abstractmethod
    def get_by_account_id(self, account_id: str):
        ...

    @abstractmethod
    def get_by_account_id_and_date(self, account_id: str, date: date):
        ...
