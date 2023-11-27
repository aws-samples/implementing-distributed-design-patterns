"""Service to release reserved inventory stock when check out fails"""
# Saga Step 1 Compensation

import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")


def handle_request(event, context):
    product_id = event.get("productId")
    quantity = int(event.get("quantity"))
    success = restock_product_item(quantity, product_id)

    if success:
        return {
            "success": False,
            "balance": False,
            "stock": True,
            "restock": True,
        }
    else:
        return {
            "success": False,
            "balance": False,
            "stock": True,
            "restock": False,
        }


def restock_product_item(checkout_quantity: int, product_id: str) -> bool:
    """Return the reserved stock to product catalogue in DynamoDb"""
    table_name = os.environ["PRODUCT_TABLE"]
    product_table = dynamodb.Table(table_name)
    try:
        response = product_table.get_item(Key={"id": product_id})
    except ClientError as e:
        print(e.response)
    item = response.get("Item", {})
    existing_stock = int(item.get("stock"), 0)
    new_stock = existing_stock + checkout_quantity  # Restock from check out
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
