from fastapi import APIRouter
from iiko.api import get_token, get_order_by_table_with_retry, add_payment, close_order
from iiko.tables import get_table_id
from database.models import create_payment, get_payment, update_payment_status
from payments.plexy import create_payment_link

router = APIRouter(prefix="/api")


@router.get("/order/{table_num}")
async def get_order(table_num: str):
    """Получить заказ по номеру стола"""
    table_id = get_table_id(table_num)
    if not table_id:
        return {"error": "Стол не найден"}
    
    token = get_token()
    orders = get_order_by_table_with_retry(token, table_id, max_attempts=5, delay=2)
    
    if not orders:
        return {"error": "Нет активных заказов"}
    
    order = orders[0]
    order_data = order["order"]
    
    items = []
    for item in order_data["items"]:
        if item["resultSum"] > 0:
            items.append({
                "name": item["product"]["name"],
                "price": item["resultSum"]
            })
    
    return {
        "order_id": order["id"],
        "table": table_num,
        "items": items,
        "total": order_data["sum"]
    }


@router.post("/pay/{table_num}")
async def pay_order(table_num: str):
    """Создать ссылку на оплату"""
    table_id = get_table_id(table_num)
    if not table_id:
        return {"error": "Стол не найден"}
    
    token = get_token()
    orders = get_order_by_table_with_retry(token, table_id, max_attempts=5, delay=2)
    
    if not orders:
        return {"error": "Нет заказа для оплаты"}
    
    order = orders[0]
    order_id = order["id"]
    order_sum = order["order"]["sum"]
    
    print(f"💰 Создаём платёж: стол {table_num}, сумма {order_sum}")
    
    result = create_payment_link(
        amount=order_sum,
        table_num=table_num,
        order_id=order_id,
        description=f"Оплата заказа - Стол {table_num}"
    )
    
    print(f"📤 Результат Plexy: {result}")
    
    if not result["success"]:
        return {"error": "Ошибка создания платежа"}
    
    create_payment(
        payment_id=result["payment_id"],
        table_num=table_num,
        order_id=order_id,
        amount=int(order_sum)
    )
    
    return {
        "success": True,
        "payment_url": result["url"]
    }