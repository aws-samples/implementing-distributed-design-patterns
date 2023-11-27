from models.point_transaction import PointTransaction
from services.point_balance_service import PointBalanceInputPort
from ports.point_transaction_input_port import PointTransactionInputPort
from ports.point_transaction_output_port import PointTransactionOutputPort
from uuid import uuid4
from datetime import datetime

class PointTransactionService(PointTransactionInputPort): 

    point_transaction_repository : PointTransactionOutputPort
    point_balance_service : PointBalanceInputPort

    def __init__(self, point_transaction_repository:PointTransactionOutputPort, point_balance_service: PointBalanceInputPort):
        self.point_transaction_repository = point_transaction_repository
        self.point_balance_service = point_balance_service

    def issue_point(self, account_id:str, amount:int) -> PointTransaction:
        point_transaction = PointTransaction(
            id=str(uuid4()),
            date_time=datetime.now().isoformat(),
            account_id=account_id,
            transaction_type="issue",     
            amount=amount
        )
        self.point_transaction_repository.save(point_transaction)
        return point_transaction
    
    def redeem_point(self, account_id:str, amount:int) -> PointTransaction:
        current_balance = self.point_balance_service.get_balance(account_id)
        point_transaction : PointTransaction = None
        if amount <= current_balance.balance: 
            point_transaction = PointTransaction(
                id = str(uuid4()),
                date_time = datetime.now().isoformat(),
                account_id = account_id,
                transaction_type = "redeem",     
                amount = amount
            )
            self.point_transaction_repository.save(point_transaction)
        else:
            raise Exception('Insufficient balance')
        return point_transaction
