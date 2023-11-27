from __future__ import print_function
import json
from services.point_transaction_service import PointTransactionService
from services.point_balance_service import PointBalanceService
from adapters.point_transaction_repository import PointTransactionRepository
from adapters.point_balance_repository import PointBalanceRepository

point_transaction_service = PointTransactionService(
    PointTransactionRepository(), 
    PointBalanceService(PointBalanceRepository())
)

# --------------- Main handler ------------------
def handle_request(event, context):
    body = json.loads(event['body'])
    account_id = body.get('account_id')
    amount = body.get('amount')
    try:
        method = event['requestContext']['httpMethod']
        if method == "POST":
            point_transaction_obj = point_transaction_service.issue_point(
                account_id = account_id,
                amount = amount
            )
        elif method == "DELETE":
            point_transaction_obj = point_transaction_service.redeem_point(
                account_id = account_id,
                amount = amount
            )
    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": e.args
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps(point_transaction_obj.__dict__, indent=4)
    }
