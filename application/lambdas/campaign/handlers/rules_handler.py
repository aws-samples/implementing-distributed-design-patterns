import os
import json
import boto3
import re
from botocore.exceptions import ClientError
from services.campaign_service import CampaignService

dynamodb = boto3.resource('dynamodb')
lambda_client = boto3.client('lambda')

table_name = os.environ['CAMPAIGN_TABLE']
function_name = os.environ['POINT_FUNCTION']
table = dynamodb.Table(table_name)
campaigns = CampaignService(table)

def handle_request(event, context):
    campaign_list = campaigns.query_campaign(event["detail"]["client"])
    total = 0
    for item in campaign_list:
        rule_list = json.loads(item["rules"])
        for rule in rule_list:
            var = rule["variable"]
            var = re.search("^[a-zA-Z\$\.]+$", var).group()
            amount = event["detail"]["total"]
            value = rule["condition"]["value"]
            formula = rule["action"]["formula"].replace(var, str(amount))
            condition = rule["condition"]["rule"]
            if (condition == "numeric_greater_than" and amount >= value) or (condition == "numeric_less_than" and amount <= value) or (condition == "numeric_equals" and amount == value): 
                #Do not do this
                points = eval(formula)
                total += points
    total = round(total)        
    function_params={
        "body": json.dumps({
            "account_id":event["detail"]["username"],
            "amount": total
        }),
        "requestContext":{
            "httpMethod": "POST"
        }
    }
    try:
        lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(function_params))
    except ClientError:
        print("Couldn't invoke function %s.", function_name)
        raise
    return {
        'statusCode': 200,
        'body': json.dumps({"total": total}),
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
        }
    }
