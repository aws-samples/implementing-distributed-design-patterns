# get_campaign_rules

import os
import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table_name = os.environ["CAMPAIGN_TABLE"]
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Get all rules
    response = table.scan()

    return {
        "statusCode": 200,
        "body": json.dumps({"items": response["Items"], "count": response["Count"]}),
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
        },
    }
