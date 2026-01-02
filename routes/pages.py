from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import time

router = APIRouter()


@router.get("/")
async def root():
    """Главная страница"""
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # Добавляем timestamp для сброса кеша
    version = int(time.time())
    html = html.replace('app.js"', f'app.js?v={version}"')
    html = html.replace('style.css"', f'style.css?v={version}"')
    
    return HTMLResponse(content=html)