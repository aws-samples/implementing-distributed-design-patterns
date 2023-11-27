from typing import List

class BalanceEntry():
    issued_date: str
    balance: int
    last_updated: str
    status: str
    
    def __init__(self, issued_date: str, balance: int, last_updated: str, status: str):
        self.issued_date = issued_date
        self.balance = balance
        self.last_updated = last_updated
        self.status = status

class PointBalance():
    account_id: str
    balance: int
    balance_entries : List[BalanceEntry]
    
    def __init__(self, account_id: str, balance: int, balance_entries: list[BalanceEntry]):
        self.account_id = account_id
        self.balance = balance
        self.balance_entries = balance_entries

    def __hash__(self):
        return hash(self.account_id)
    
