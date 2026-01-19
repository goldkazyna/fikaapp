from fastapi import APIRouter, Request
from datetime import datetime
import requests

router = APIRouter(prefix="/api")

# Тестовый канал для отзывов
TELEGRAM_BOT_TOKEN = "8224039811:AAF_ONgVzNpsZap4Xf_csteZvo2DLdB3dZY"
CHANNEL_ID = "-1003598950701"


@router.post("/rating")
async def save_rating(request: Request):
    """Сохранить оценку и отправить в Telegram"""
    data = await request.json()
    
    rating = data.get("rating", 0)
    comment = data.get("comment", "")
    table = data.get("table", "")
    user = data.get("user", "Гость")
    
    # Формируем звёзды
    stars = "⭐" * rating + "☆" * (5 - rating)
    
    # Формируем сообщение
    message = f"🆕 <b>Новый отзыв</b>\n\n"
    message += f"👤 {user}\n"
    message += f"🪑 Стол: {table}\n"
    message += f"📊 Оценка: {stars}\n"
    if comment:
        message += f"\n💬 <i>{comment}</i>"
    
    # Отправляем в Telegram канал
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": CHANNEL_ID,
                "text": message,
                "parse_mode": "HTML"
            }
        )
        print(f"✅ Отзыв отправлен в канал")
    except Exception as e:
        print(f"❌ Ошибка отправки в канал: {e}")
    
    # Сохраняем в файл
    with open("database/ratings.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} | Стол: {table} | Оценка: {rating}⭐ | {user} | {comment}\n")
    
    print(f"⭐ Новая оценка: {rating} звёзд от {user} (стол {table})")
    
    return {"success": True}