import boto3
import os

from ports.point_transaction_output_port import PointTransactionOutputPort
from models.point_transaction import PointTransaction

class PointTransactionRepository(PointTransactionOutputPort):
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(os.environ['POINT_TRANSACTION_TABLE'])

    def save(self, item: PointTransaction):
        self.table.put_item(Item=vars(item))

    def get_by_id(self, id):
        response = self.table.get_item(Key={'id': id})
        return response.get('Item')

    def delete(self, id):
        self.table.delete_item(Key={'id': id})

    def update(self, item):
        self.table.update_item(
            Key={'id': item['id']},
            UpdateExpression="set points=:p, status=:s",
            ExpressionAttributeValues={
                ':p': item['points'],
                ':s': item['status']
            },
            ReturnValues="UPDATED_NEW"
        )