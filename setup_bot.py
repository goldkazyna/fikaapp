import requests

BOT_TOKEN = "8432178512:AAFkDlVLysxmwp0NtxDsquQXfh4EAXzqaFM"
WEBAPP_URL = "https://unpersecuted-supervictoriously-christene.ngrok-free.dev?table=65"

# Устанавливаем кнопку меню
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