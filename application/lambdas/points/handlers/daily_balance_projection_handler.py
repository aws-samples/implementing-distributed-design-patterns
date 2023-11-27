import datetime

from services.point_balance_service import PointBalanceService
from adapters.point_balance_repository import PointBalanceRepository

point_balance_service = PointBalanceService(PointBalanceRepository())

def handle_records(event, context):
    for record in event.get("Records", []):
        # only process 'append' only events
        if record['eventName'] == 'INSERT':
            new_image = record['dynamodb']['NewImage']
            transaction_id = new_image['id']['S']
            transaction_type = new_image['transaction_type']['S']
            amount_tobe_updated = int(new_image['amount']['N'])
            updated_datetime = datetime.datetime.fromisoformat(new_image['date_time']['S'])
            account_id = new_image['account_id']['S']

            if transaction_type == "issue":
                point_balance_service.issue(
                    account_id=account_id,
                    amount=amount_tobe_updated,
                    transaction_id=transaction_id,
                    updated_datetime=updated_datetime
                )
            elif transaction_type == "redeem":
                point_balance_service.redeem(
                    account_id=account_id,
                    amount=amount_tobe_updated,
                    transaction_id=transaction_id,
                    updated_datetime=updated_datetime
                )
            else:
                print("Unknown transaction type")
                raise
