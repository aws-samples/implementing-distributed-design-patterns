from __future__ import print_function

import json

from services.point_balance_service import PointBalanceService
from adapters.point_balance_repository import PointBalanceRepository

point_balance_service = PointBalanceService(PointBalanceRepository())

# --------------- Main handler ------------------
def handle_request(event, context):
    account_id = event.get("queryStringParameters", {}).get('account_id', None)
    point_balance = point_balance_service.get_balance(account_id)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps(point_balance, default=lambda o: o.__dict__, indent=4)
    }
