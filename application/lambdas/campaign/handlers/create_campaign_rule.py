# create_campaign_rule

import os
import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table_name = os.environ["CAMPAIGN_TABLE"]
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    body = json.loads(event["body"])
    client = body.get("client", None)
    campaign_name = body.get("campaign_name", None)
    rules = body.get("rules", None)
    try:
        response = table.put_item(
            Item={
                "client": client,
                "campaign_name": campaign_name,
                "status": "active",
                "rules": rules,
            }
        )
    except ClientError as e:
        print(e.response)

    return {
        "statusCode": 200,
        "body": json.dumps(response),
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
        },
    }
