"""Service to reserve inventory stock during check out"""
# Saga Step 1 Transaction

import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table_name = os.environ["PRODUCT_TABLE"]
product_table = dynamodb.Table(table_name)


def handle_request(event, context):
    username = event.get("userId")
    product_id = event.get("productId")
    quantity = int(event.get("quantity"))

    existing_stock = get_product_stock(product_id)
    if existing_stock >= quantity:
        success = reserve_stock_for_checkout(existing_stock, quantity, product_id)
        if success:
            data = {
                "success": True,
                "stock": True,
                "userId": username,
                "quantity": quantity,
                "productId": product_id,
            }
        else:
            raise
        return data

    else:
        # insufficient stock for check out!
        return {
            "success": False,
            "stock": False,
            "quantity": quantity,
            "productId": product_id,
        }


def get_product_stock(product_id: str) -> int:
    """Retrieve product stock data from DynamoDB"""
    try:
        response = product_table.get_item(Key={"id": product_id})
    except ClientError as e:
        print(e.response)
    item = response.get("Item", {})
    return int(item.get("stock"), 0)


def reserve_stock_for_checkout(
    existing_stock: int, quantity: int, product_id: str
) -> bool:
    """Deduct product stock value in DynamoDB"""
    new_stock = existing_stock - quantity  # Take stock for check out
    attribute_values = {":new_stock": str(new_stock)}
    update_expression = "SET stock=:new_stock"
    try:
        product_table.update_item(
            Key={"id": product_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=attribute_values,
        )
        return True
    except ClientError as e:
        print(e.response)
        return False
