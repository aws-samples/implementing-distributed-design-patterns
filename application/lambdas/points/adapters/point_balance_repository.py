import boto3
import os

from boto3.dynamodb.conditions import Key
from ports.point_balance_output_port import PointBalanceOutputPort

from datetime import date

class PointBalanceRepository(PointBalanceOutputPort):
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.client = boto3.client('dynamodb')
        self.table_name = os.environ['DAILY_BALANCE_TABLE']
        self.table = self.dynamodb.Table(self.table_name)

    def save(self, item):
        try:
            self.table.put_item(
                Item=item,
                ConditionExpression='attribute_not_exists(account_id) AND attribute_not_exists(issued_date)'
            )
        except:
            print("Concurrent insert detected!!!, fallback to update")
            self.update_account_balance_by_date(item)

    def update_account_balance_by_date(self, item):
        self.table.update_item(
            Key={
                'account_id': item['account_id'],
                'issued_date': item['issued_date'],
            },
            UpdateExpression="add balance :amount SET last_updated = :date_time, transaction_ids = list_append(transaction_ids, :transaction_ids)",
            ExpressionAttributeValues={
                ':amount': item['balance'],
                ':date_time': item['last_updated'],
                ':transaction_ids': item['transaction_ids'],
            },
            ReturnValues="UPDATED_NEW"
        )
    
    def deduct_account_balance(self, redemption_entries):
        transaction_items = []
        for item in redemption_entries:
            transaction_items.append({
                'Update': {
                    'TableName': self.table_name,
                    'Key': {
                        'account_id': {
                            'S': item['account_id']
                        },
                        'issued_date': {
                            'S': item['issued_date']
                        }
                    },
                    'UpdateExpression': "add balance :amount SET last_updated = :date_time, transaction_ids = list_append(transaction_ids, :transaction_ids)",
                    'ExpressionAttributeValues': {
                        ':amount': {
                            'N': str(-item['amount'])
                        },
                        ':date_time': {
                            'S': item['updated_datetime']
                        },
                        ':transaction_ids': {
                            'L': [{ 'S' : item['transaction_id']}]
                        }
                    }
                }
            })
        self.client.transact_write_items(
            TransactItems=transaction_items
        )

    def get_by_account_id(self, account_id: str):
        response = self.table.query(
            KeyConditionExpression=Key('account_id').eq(account_id)
        )
        return response['Items']
    
    def get_by_account_id_and_date(self, account_id: str, issued_date: date):
        response = self.table.get_item(
            Key={
                'account_id': account_id,
                'issued_date': str(issued_date)
            }
        )
        if not 'Item' in response:
            return None
        return response['Item']