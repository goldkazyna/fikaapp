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
                background: #1c1c1d;
                color: #ffffff;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 20px;
            }}
            .container {{ max-width: 400px; width: 100%; }}
            .icon {{ font-size: 80px; margin-bottom: 20px; }}
            .title {{ font-size: 24px; font-weight: 700; margin-bottom: 10px; }}
            .subtitle {{ color: #8e8e93; font-size: 16px; margin-bottom: 30px; }}
            
            .rating-section {{
                background: #2c2c2e;
                border-radius: 16px;
                padding: 20px;
                margin-bottom: 20px;
            }}
            .rating-title {{
                font-size: 16px;
                margin-bottom: 16px;
                color: #8e8e93;
            }}
            .stars {{
                display: flex;
                justify-content: center;
                gap: 8px;
                margin-bottom: 16px;
            }}
            .star {{
                font-size: 36px;
                cursor: pointer;
                transition: transform 0.2s;
                color: #3a3a3c;
            }}
            .star.active {{
                color: #ffd700;
            }}
            .star:hover {{
                transform: scale(1.2);
            }}
            
            .comment-input {{
                width: 100%;
                background: #3a3a3c;
                border: none;
                border-radius: 12px;
                padding: 14px 16px;
                color: #ffffff;
                font-size: 16px;
                resize: none;
                min-height: 80px;
                margin-bottom: 16px;
            }}
            .comment-input::placeholder {{
                color: #8e8e93;
            }}
            .comment-input:focus {{
                outline: none;
            }}
            
            .btn {{
                width: 100%;
                background: #3b82f6;
                border: none;
                border-radius: 12px;
                padding: 16px 32px;
                color: #fff;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                margin-bottom: 12px;
            }}
            .btn:disabled {{
                background: #3a3a3c;
                color: #8e8e93;
            }}
            .btn-secondary {{
                background: #2c2c2e;
            }}
            
            .thanks {{
                display: none;
                color: #30d158;
                font-size: 18px;
                font-weight: 600;
                margin-top: 16px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="icon">✅</div>
            <div class="title">Оплата прошла успешно!</div>
            <div class="subtitle">Спасибо за заказ в FIKA</div>
            
            <div class="rating-section" id="rating-section">
                <div class="rating-title">Оцените ваш визит</div>
                <div class="stars" id="stars">
                    <span class="star" data-rating="1">★</span>
                    <span class="star" data-rating="2">★</span>
                    <span class="star" data-rating="3">★</span>
                    <span class="star" data-rating="4">★</span>
                    <span class="star" data-rating="5">★</span>
                </div>
                <textarea class="comment-input" id="comment" placeholder="Ваш комментарий (необязательно)"></textarea>
                <button class="btn" id="btn-send" disabled onclick="sendRating()">Отправить оценку</button>
            </div>
            
            <div class="thanks" id="thanks">Спасибо за вашу оценку! 🙏</div>
            
            <button class="btn btn-secondary" onclick="closeApp()">Закрыть</button>
        </div>
        <script>
            const tg = window.Telegram.WebApp;
            tg.ready();
            tg.expand();
            
            let selectedRating = 0;
            const stars = document.querySelectorAll('.star');
            const btnSend = document.getElementById('btn-send');
            
            stars.forEach(star => {{
                star.addEventListener('click', () => {{
                    selectedRating = parseInt(star.dataset.rating);
                    updateStars();
                    btnSend.disabled = false;
                }});
            }});
            
            function updateStars() {{
                stars.forEach(star => {{
                    const rating = parseInt(star.dataset.rating);
                    star.classList.toggle('active', rating <= selectedRating);
                }});
            }}
            
            async function sendRating() {{
                const comment = document.getElementById('comment').value;
                const table = '{table}';
                
                btnSend.disabled = true;
                btnSend.textContent = 'Отправка...';
                
                try {{
                    await fetch('/api/rating', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{
                            table: table,
                            rating: selectedRating,
                            comment: comment,
                            user: tg.initDataUnsafe?.user?.first_name || 'Гость'
                        }})
                    }});
                }} catch (e) {{
                    console.log('Rating error:', e);
                }}
                
                document.getElementById('rating-section').style.display = 'none';
                document.getElementById('thanks').style.display = 'block';
            }}
            
            function closeApp() {{
                tg.close();
            }}
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
                background: #1c1c1d;
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
            .subtitle {{ color: #8e8e93; font-size: 16px; margin-bottom: 30px; }}
            .btn {{
                background: #2c2c2e;
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