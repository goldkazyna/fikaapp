import requests
from datetime import datetime, timedelta
import time

API_KEY = "pr_aed2ba5872c5407f99da2947fbe1bbaf"
BASE_URL = "https://api.plexypay.com/v1"

# Продакшен
PROD_URL = "https://fikaapp.kz"
WEBHOOK_URL = f"{PROD_URL}/api/webhook/plexy"
SUCCESS_URL = f"{PROD_URL}/success"
FAIL_URL = f"{PROD_URL}/fail"


def create_payment_link(amount: int, table_num: str, order_id: str, description: str):
    """Создать ссылку на оплату"""
    expires = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Уникальный reference с timestamp
    timestamp = int(time.time() * 1000)
    order_reference = f"t{table_num}_{timestamp}"
    
    response = requests.post(
        f"{BASE_URL}/payment-links",
        headers={
            "Authorization": API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "amount": int(amount * 100),
            "currency": "KZT",
            "description": description,
            "orderReference": order_reference,
            "expiresAt": expires,
            "validation": False,
            "autoClearing": True,
            "metadata": {
                "successUrl": f"{SUCCESS_URL}?table={table_num}",
                "failureUrl": f"{FAIL_URL}?table={table_num}",
                "callbackUrl": WEBHOOK_URL
            }
        }
    )
    
    if response.status_code == 201:
        data = response.json()
        return {
            "success": True,
            "payment_id": data["id"],
            "url": data["url"]
        }
    else:
        return {
            "success": False,
            "error": response.text
        }