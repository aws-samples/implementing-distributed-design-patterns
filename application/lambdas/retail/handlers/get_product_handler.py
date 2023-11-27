"""Service to get product details"""

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
    product_id = event.get("pathParameters").get("id")
    dynamodb = boto3.resource("dynamodb")
    table_name = os.environ["PRODUCT_TABLE"]
    table = dynamodb.Table(table_name)
    try:
        response = table.get_item(Key={"id": product_id})
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
