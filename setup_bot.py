import requests

BOT_TOKEN = "8432178512:AAFkDlVLysxmwp0NtxDsquQXfh4EAXzqaFM"
WEBAPP_URL = "https://fikaapp.kz?table=65"

response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setChatMenuButton",
    json={
        "menu_button": {
            "type": "web_app",
            "text": "Открыть",
            "web_app": {"url": WEBAPP_URL}
        }
    }
)

print(response.json())