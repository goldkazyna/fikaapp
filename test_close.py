import requests

API_KEY = "679e0daeba1c45d2b38ad8e3e61de32d"
ORG_ID = "fe680633-a3d5-4e1a-a376-3b11969dad92"

ORDER_ID = "85b07628-0611-484d-b30f-0f49cc0ccb51"

# 1. Получаем токен
response = requests.post(
    "https://api-ru.iiko.services/api/1/access_token",
    json={"apiLogin": API_KEY}
)
token = response.json()["token"]
print("✅ Токен получен")

# 2. Закрываем заказ
response = requests.post(
    "https://api-ru.iiko.services/api/1/order/close",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "organizationId": ORG_ID,
        "orderId": ORDER_ID
    }
)
print("\n🔒 Закрытие заказа:")
print(response.text)