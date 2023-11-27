from abc import ABC, abstractmethod
from models.point_balance import PointBalance

from datetime import datetime

class PointBalanceInputPort(ABC):

    @abstractmethod
    def issue(self, account_id:str, updated_datetime:datetime, amount:int, transaction_id:str) -> PointBalance :
        ...

    @abstractmethod
    def redeem(self, account_id:str, updated_datetime:datetime, amount:int, transaction_id:str) -> PointBalance :
        ...

    @abstractmethod
    def get_balance(self, account_id:str) -> PointBalance :
        ...
