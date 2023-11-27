class PointTransaction():

    id: str
    date_time: str
    account_id: str
    transaction_type: str
    amount: int
    
    def __init__(self, id:str, date_time: str, account_id: str, transaction_type: str, amount: int):
        self.id = id
        self.date_time = date_time
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.amount = amount

    def __hash__(self):
        return hash(self.id)