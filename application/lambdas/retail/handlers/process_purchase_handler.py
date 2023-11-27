import os
import json
import boto3
from botocore.exceptions import ClientError


def handle_request(event, context):
    sf = boto3.client("stepfunctions")
    
    purchase_state_machine = os.environ["PURCHASE_STATE_MACHINE"]
    response = sf.start_sync_execution(stateMachineArn=purchase_state_machine, input=event["body"])

    return {
        "statusCode": 200,
        "body": json.dumps(response, indent=4, sort_keys=True, default=str),
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
        },
    }
