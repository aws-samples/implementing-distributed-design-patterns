from abc import ABC, abstractmethod

from models.point_transaction import PointTransaction

class PointTransactionInputPort(ABC):

    @abstractmethod
    def issue_point(self, account_id:str, transaction_type:str, amount:int) -> PointTransaction:
        ...
    @abstractmethod
    def redeem_point(self, account_id:str, transaction_type:str, amount:int) -> PointTransaction:
        ...