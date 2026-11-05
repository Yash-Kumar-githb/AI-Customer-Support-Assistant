import json
from pathlib import Path
from langchain.tools import tool

# Find the orders.json file
ORDER_FILE = Path(__file__).resolve().parent.parent / "data" / "orders.json"


@tool
def check_order_status(order_id: str) -> str:
    """Get customer order details using order ID."""

    # Open orders.json and convert JSON into Python dictionary
    with open(ORDER_FILE, "r", encoding="utf-8") as file:
        orders = json.load(file)

    # Remove extra spaces and convert ID to uppercase
    order_id = order_id.strip().upper()

    # Search for the order ID in the dictionary
    order = orders.get(order_id)

    # If order ID doesn't exist
    if not order:
        return "Order not found"

    # If order exists, return its details
    return (
        f"Order ID: {order_id}\n"
        f"Customer: {order['customer_name']}\n"
        f"Status: {order['status']}\n"
        f"Expected Delivery: {order['expected_delivery']}"
    )


# Test the tool
if __name__ == "__main__":
    print(check_order_status.invoke({"order_id": "ORD123"}))