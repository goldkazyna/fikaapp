import requests
import time
from config import API_KEY, ORG_ID, TERMINAL_ID, IIKO_API_URL, CASH_PAYMENT


def get_token():
    """Получить токен доступа"""
    response = requests.post(
        f"{IIKO_API_URL}/access_token",
        json={"apiLogin": API_KEY}
    )
    return response.json()["token"]


def init_table(token, table_id):
    """Инициализировать стол (синхронизация с Cloud)"""
    requests.post(
        f"{IIKO_API_URL}/order/init_by_table",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "organizationId": ORG_ID,
            "terminalGroupId": TERMINAL_ID,
            "tableIds": [table_id]
        }
    )


def get_order_by_table(token, table_id):
    """Получить заказ по столу"""
    response = requests.post(
        f"{IIKO_API_URL}/order/by_table",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "organizationIds": [ORG_ID],
            "tableIds": [table_id],
            "statuses": ["New", "Bill"]
        }
    )
    return response.json().get("orders", [])


def get_order_by_table_with_retry(token, table_id, max_attempts=5, delay=2):
    """Получить заказ с повторными попытками"""
    for attempt in range(max_attempts):
        # Инициализируем стол
        init_table(token, table_id)
        
        # Ждём синхронизацию
        time.sleep(delay)
        
        # Пробуем получить заказ
        orders = get_order_by_table(token, table_id)
        
        if orders:
            return orders
        
        print(f"⏳ Попытка {attempt + 1}/{max_attempts} — заказ не найден, повторяем...")
    
    return []


def add_payment(token, order_id, amount):
    """Добавить оплату к заказу"""
    requests.post(
        f"{IIKO_API_URL}/order/add_payments",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "organizationId": ORG_ID,
            "orderId": order_id,
            "payments": [
                {
                    "paymentTypeId": CASH_PAYMENT,
                    "sum": amount,
                    "paymentTypeKind": "Cash"
                }
            ]
        }
    )


def close_order(token, order_id):
    """Закрыть заказ"""
    requests.post(
        f"{IIKO_API_URL}/order/close",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "organizationId": ORG_ID,
            "orderId": order_id
        }
    )