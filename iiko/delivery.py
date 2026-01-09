import requests
from datetime import datetime, timedelta
from config import API_KEY, ORG_ID, TERMINAL_ID, IIKO_API_URL

ORDER_TYPE_PICKUP = "5b1508f9-fe5b-d6af-cb8d-043af587d5c2"
CASH_PAYMENT = "09322f46-578a-d210-add7-eec222a08871"


def get_token():
    response = requests.post(
        f"{IIKO_API_URL}/access_token",
        json={"apiLogin": API_KEY}
    )
    return response.json()["token"]


def create_pickup_order(customer_name: str, customer_phone: str, items: list, total: float):
    """Создать заказ на самовывоз
    
    items: [{"id": "product_id", "amount": 1, "price": 5200}, ...]
    """
    token = get_token()
    
    complete_before = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
    
    # Формируем позиции заказа
    order_items = []
    for item in items:
        order_items.append({
            "productId": item["id"],
            "type": "Product",
            "amount": item["amount"]
        })
    
    order_data = {
        "organizationId": ORG_ID,
        "terminalGroupId": TERMINAL_ID,
        "order": {
            "orderTypeId": ORDER_TYPE_PICKUP,
            "customer": {
                "name": customer_name,
                "phone": customer_phone
            },
            "phone": customer_phone,
            "completeBefore": complete_before,
            "items": order_items,
            "payments": [
                {
                    "paymentTypeId": CASH_PAYMENT,
                    "paymentTypeKind": "Cash",
                    "sum": total,
                    "isProcessedExternally": True
                }
            ]
        }
    }
    
    response = requests.post(
        f"{IIKO_API_URL}/deliveries/create",
        headers={"Authorization": f"Bearer {token}"},
        json=order_data
    )
    
    if response.status_code == 200:
        data = response.json()
        return {
            "success": True,
            "order_id": data["orderInfo"]["id"]
        }
    else:
        return {
            "success": False,
            "error": response.text
        }