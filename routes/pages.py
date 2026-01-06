from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import time

router = APIRouter()


@router.get("/")
async def root():
    """Главная страница"""
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    version = int(time.time())
    html = html.replace('app.js"', f'app.js?v={version}"')
    html = html.replace('style.css"', f'style.css?v={version}"')
    
    return HTMLResponse(content=html)


@router.get("/success")
async def success_page(table: str = ""):
    """Страница успешной оплаты"""
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Оплачено - FIKA</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #0a0a0a;
                color: #ffffff;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 20px;
            }}
            .container {{ max-width: 400px; }}
            .icon {{ font-size: 80px; margin-bottom: 20px; }}
            .title {{ font-size: 24px; font-weight: 700; margin-bottom: 10px; }}
            .subtitle {{ color: #888; font-size: 16px; margin-bottom: 30px; }}
            .btn {{
                background: linear-gradient(135deg, #22c55e, #16a34a);
                border: none;
                border-radius: 12px;
                padding: 16px 32px;
                color: #fff;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="icon">✅</div>
            <div class="title">Оплата прошла успешно!</div>
            <div class="subtitle">Спасибо за заказ в FIKA</div>
            <button class="btn" onclick="closeApp()">Закрыть</button>
        </div>
        <script>
            const tg = window.Telegram.WebApp;
            tg.ready();
            
            function closeApp() {{
                tg.close();
            }}
            
            // Автозакрытие через 5 секунд
            setTimeout(() => tg.close(), 5000);
        </script>
    </body>
    </html>
    '''
    return HTMLResponse(content=html)


@router.get("/fail")
async def fail_page(table: str = ""):
    """Страница неудачной оплаты"""
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ошибка - FIKA</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #0a0a0a;
                color: #ffffff;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 20px;
            }}
            .container {{ max-width: 400px; }}
            .icon {{ font-size: 80px; margin-bottom: 20px; }}
            .title {{ font-size: 24px; font-weight: 700; margin-bottom: 10px; color: #ef4444; }}
            .subtitle {{ color: #888; font-size: 16px; margin-bottom: 30px; }}
            .btn {{
                background: #1a1a1a;
                border: none;
                border-radius: 12px;
                padding: 16px 32px;
                color: #fff;
                font-size: 16px;
                cursor: pointer;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="icon">❌</div>
            <div class="title">Ошибка оплаты</div>
            <div class="subtitle">Попробуйте ещё раз</div>
            <button class="btn" onclick="closeApp()">Закрыть</button>
        </div>
        <script>
            const tg = window.Telegram.WebApp;
            tg.ready();
            
            function closeApp() {{
                tg.close();
            }}
        </script>
    </body>
    </html>
    '''
    return HTMLResponse(content=html)