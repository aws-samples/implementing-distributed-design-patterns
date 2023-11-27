"""Service to simulate payment processing"""
# Saga Step 2 Transaction

import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
user_wallet_table_name = os.environ["USER_WALLET_BALANCE_TABLE"]
product_table_name = os.environ["PRODUCT_TABLE"]
user_wallet_table = dynamodb.Table(user_wallet_table_name)
product_table = dynamodb.Table(product_table_name)


def handle_request(event, context):
    username = event.get("userId")
    product_id = event.get("productId")
    quantity = int(event.get("quantity"))

    price = get_product_price(product_id)
    user_balance = get_user_wallet_balance(username)
    # Quick checkout purchases multiple quantities of 1 product at a time
    bill_total = calculate_bill_product_total(price, quantity)
    if user_balance >= bill_total:
        success = deduct_user_wallet_balance(user_balance, bill_total, username)
        if success:
            data = {"success": True, "stock": True, "balance": True, "username": username,
            "quantity": quantity,
            "productId": product_id,
            "total": bill_total,
            "client": "UnicornStore"}
        else:
            raise
        return data

    else:
        # insufficient balance!
        return {
            "success": False,
            "balance": False,
            "username": username,
            "quantity": quantity,
            "productId": product_id,
            "success": False,
            "balance": False,
            "username": username,
            "quantity": quantity,
            "productId": product_id,
        }


def calculate_bill_product_total(unit_price: int, quantity: int) -> int:
    """Calculate the total cost for one product based on quanitty and unit price"""
    return unit_price * quantity


def get_product_price(product_id: str) -> int:
    """Retrieve product price data from DynamoDB"""
    try:
        response = product_table.get_item(Key={"id": product_id})
    except ClientError as e:
        print(e.response)
    item = response.get("Item", {})
    return int(item.get("price"), 0)


def get_user_wallet_balance(username: str) -> int:
    """Retrieve user wallet balance from DynamoDB"""
    try:
        response = user_wallet_table.get_item(Key={"username": username})
    except ClientError as e:
        print(e.response)
    item = response.get("Item", {})
    return int(item.get("balance"), 0)



def deduct_user_wallet_balance(
    user_balance: int, bill_total: int, username: str
) -> bool:
    """Deduct the total cost from the user balance in DynamoDB"""
    new_balance = user_balance - bill_total  # Deduct balance
    attribute_values = {":new_balance": str(new_balance)}
    update_expression = "SET balance=:new_balance"
    try:
        user_wallet_table.update_item(
            Key={"username": username},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=attribute_values,
        )
        return True
    except ClientError as e:
        print(e.response)
        return False
