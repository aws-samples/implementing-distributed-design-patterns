import logging
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class CampaignService:
    def __init__(self, table):
        self.table = table
    def get_campaign(self, client, campaign_name):
        # Get single campaign 
        try:
            response = self.table.get_item(Key={'client': client, 'campaign_name': campaign_name})
        except ClientError as err:
            logger.error(
                "Input: Client: %s Table: %s Campaign: %s Error: %s: %s",
                client, self.table.name, campaign_name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response['Item']


    # snippet-start:[python.example_code.dynamodb.Query]
    def query_campaign(self, client):
        """
        Query on client to match mutliple
        """
        try:
            response = self.table.query(KeyConditionExpression=Key('client').eq(client))
        except ClientError as err:
            logger.error(
                "Input: (client: %s)   Error: %s  %s", client,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response['Items']
        
    def update_campaign_status(self, client, campaign_name, status):
        try:
            response = self.table.update_item(
                Key={'client': client, 'campaign_name': campaign_name},
                UpdateExpression="set status=:r",
                ExpressionAttributeValues={
                    ':r': status},
                ReturnValues="UPDATED_NEW")
        except ClientError as err:
            logger.error(
                "Couldn't update movie %s in table %s. Here's why: %s: %s",
                client, self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response['Attributes']

    # snippet-end:[python.example_code.dynamodb.UpdateItem.UpdateExpression]