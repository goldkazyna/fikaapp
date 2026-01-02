import requests
import time

API_KEY = "679e0daeba1c45d2b38ad8e3e61de32d"
ORG_ID = "fe680633-a3d5-4e1a-a376-3b11969dad92"
TERMINAL_ID = "7641870b-66fb-01b4-018c-8af7de070064"
TABLE_65 = "b76f1f9d-55f4-4380-843c-821a1d09c41a"

# 1. Получаем токен
response = requests.post(
    "https://api-ru.iiko.services/api/1/access_token",
    json={"apiLogin": API_KEY}
)
token = response.json()["token"]
print("✅ Токен получен")

# 2. Init
response = requests.post(
    "https://api-ru.iiko.services/api/1/order/init_by_table",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "organizationId": ORG_ID,
        "terminalGroupId": TERMINAL_ID,
        "tableIds": [TABLE_65]
    }
)
print("\n📤 Init by table:")
print(response.text)

# 3. Ждём синхронизацию
print("\n⏳ Ждём 2 секунды...")
time.sleep(2)

# 4. Получаем заказ
response = requests.post(
    "https://api-ru.iiko.services/api/1/order/by_table",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "organizationIds": [ORG_ID],
        "tableIds": [TABLE_65],
        "statuses": ["New", "Bill"]
    }
)
print("\n📋 Заказы на столе 65:")
print(response.text)