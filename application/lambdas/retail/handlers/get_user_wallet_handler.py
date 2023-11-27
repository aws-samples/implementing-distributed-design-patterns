"""Service to get user wallet balance"""

import os
import json
import boto3
from botocore.exceptions import ClientError

from decimal import Decimal

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def handle_request(event, context):
    username = event.get("pathParameters").get("username")
    dynamodb = boto3.resource("dynamodb")
    table_name = os.environ["USER_WALLET_BALANCE_TABLE"]
    table = dynamodb.Table(table_name)
    try:
        response = table.get_item(Key={"username": username})
    except ClientError as e:
        print(e.response)
    item = response.get("Item", {})
    return {
        "statusCode": 200,
        "body": json.dumps(item, cls=JSONEncoder),
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
        },
    }
