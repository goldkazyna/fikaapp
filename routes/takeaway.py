from fastapi import APIRouter, Request
from iiko.delivery import create_pickup_order
from payments.plexy import create_payment_link
from database.models import create_payment

router = APIRouter(prefix="/api")


@router.post("/takeaway/checkout")
async def checkout_takeaway(request: Request):
    """Оформить заказ на самовывоз"""
    data = await request.json()
    
    customer_name = data.get("name", "Гость")
    customer_phone = data.get("phone", "")
    items = data.get("items", [])
    total = data.get("total", 0)
    
    if not items:
        return {"error": "Корзина пуста"}
    
    if not customer_phone:
        return {"error": "Укажите телефон"}
    
    # Создаём ссылку на оплату
    import time
    order_ref = f"takeaway_{int(time.time() * 1000)}"
    
    result = create_payment_link(
        amount=total,
        table_num="takeaway",
        order_id=order_ref,
        description=f"Самовывоз - {customer_name}"
    )
    
    if not result["success"]:
        return {"error": "Ошибка создания платежа"}
    
    # Сохраняем данные заказа в базу для webhook
    create_payment(
        payment_id=result["payment_id"],
        table_num="takeaway",
        order_id=order_ref,
        amount=int(total)
    )
    
    # Сохраняем детали заказа для создания после оплаты
    # Пока в файл, потом можно в базу
    import json
    order_details = {
        "payment_id": result["payment_id"],
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "items": items,
        "total": total
    }
    
    with open(f"database/{order_ref}.json", "w", encoding="utf-8") as f:
        json.dump(order_details, f, ensure_ascii=False)
    
    return {
        "success": True,
        "payment_url": result["url"],
        "order_ref": order_ref
    }