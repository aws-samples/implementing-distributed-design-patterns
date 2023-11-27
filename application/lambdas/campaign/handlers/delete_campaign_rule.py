# delete_campaign_rule

import os
import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['CAMPAIGN_TABLE']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    campaign_name = event.get("pathParameters").get("campaign_name")
    client = event.get("queryStringParameters").get("client")
    try:
        response = table.delete_item(Key={"client": client, "campaign_name": campaign_name})
    except ClientError as e:
        print(e.response)

    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*'
        }
    }
