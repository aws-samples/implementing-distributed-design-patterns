import os
from ports.point_balance_input_port import PointBalanceInputPort
from ports.point_balance_output_port import PointBalanceOutputPort
from models.point_balance import PointBalance
from models.point_balance import BalanceEntry
from datetime import datetime, date, timedelta

class PointBalanceService(PointBalanceInputPort): 

    point_balance_repository : PointBalanceOutputPort

    def __init__(self, point_query_repository:PointBalanceOutputPort):
        self.point_balance_repository = point_query_repository

    def issue(self, account_id:str, updated_datetime:datetime, amount:int, transaction_id:str) -> PointBalance:
        current_balance = self.point_balance_repository.get_by_account_id_and_date(account_id, updated_datetime.date())
        item = {
            'account_id': account_id,
            'issued_date': str(updated_datetime.date()),
            'balance': amount,
            'last_updated': updated_datetime.isoformat(),
            'transaction_ids': [transaction_id],
        }

        if current_balance is None:
            self.point_balance_repository.save(item)
        else:
            if not transaction_id in current_balance['transaction_ids']:
                # Issue new daily balance
                self.point_balance_repository.update_account_balance_by_date(item)

    def redeem(self, account_id:str, updated_datetime:datetime, amount:int, transaction_id:str) -> PointBalance :
        balance_entries = self.point_balance_repository.get_by_account_id(account_id=account_id)
        remaining_amount = amount
        redemption_entries = []
        for item in balance_entries:
            points_entry_balance = item['balance']
            issued_date = item['issued_date']
            if points_entry_balance >= remaining_amount:
                redemption_entries.append({
                    'account_id': account_id,
                    'issued_date': issued_date,
                    'amount': remaining_amount,
                    'transaction_id': transaction_id,
                    'updated_datetime': updated_datetime.isoformat()
                })
                break
            else:
                remaining_amount = remaining_amount - points_entry_balance
                redemption_entries.append({
                    'account_id': account_id,
                    'issued_date': issued_date,
                    'amount': points_entry_balance,
                    'transaction_id': transaction_id,
                    'updated_datetime': updated_datetime.isoformat()
                })
                continue
        self.point_balance_repository.deduct_account_balance(redemption_entries)
        print('AccountID: %s, Tx: %s, Daily balance redeemed!' % (account_id, transaction_id))

    def get_balance(self, account_id:str) -> PointBalance:
        items = self.point_balance_repository.get_by_account_id(account_id)
        balance = 0
        balance_entries = []

        point_ttl = int(os.environ["POINT_TTL"])
        expiring_date = date.today() - timedelta(days=point_ttl)

        for item in items:
            points_entry_balance = int(item['balance'])
            issued_date = item['issued_date']
            last_updated = item['last_updated']
            if date.fromisoformat(issued_date) <= expiring_date:
                balance_entries.append(
                    BalanceEntry(
                        issued_date=issued_date,
                        balance=points_entry_balance,
                        last_updated=last_updated,
                        status='expired'
                    )
                )
            else:
                balance = balance + points_entry_balance
                balance_entries.append(
                    BalanceEntry(
                        issued_date=issued_date,
                        balance=points_entry_balance,
                        last_updated=last_updated,
                        status='active'
                    )
                )
            
        return PointBalance(
            account_id=account_id, 
            balance= balance,
            balance_entries=balance_entries
        )