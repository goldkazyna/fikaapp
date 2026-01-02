from fastapi import APIRouter
from iiko.api import get_token, init_table, get_order_by_table, add_payment, close_order
from iiko.tables import get_table_id

router = APIRouter(prefix="/api")


@router.get("/order/{table_num}")
async def get_order(table_num: str):
    """Получить заказ по номеру стола"""
    table_id = get_table_id(table_num)
    if not table_id:
        return {"error": "Стол не найден"}
    
    token = get_token()
    init_table(token, table_id)
    
    orders = get_order_by_table(token, table_id)
    
    if not orders:
        return {"error": "Нет активных заказов"}
    
    order = orders[0]
    order_data = order["order"]
    
    # Формируем ответ
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
    """Оплатить и закрыть заказ"""
    table_id = get_table_id(table_num)
    if not table_id:
        return {"error": "Стол не найден"}
    
    token = get_token()
    init_table(token, table_id)
    
    orders = get_order_by_table(token, table_id)
    
    if not orders:
        return {"error": "Нет заказа для оплаты"}
    
    order = orders[0]
    order_id = order["id"]
    order_sum = order["order"]["sum"]
    
    # Добавляем оплату и закрываем
    add_payment(token, order_id, order_sum)
    close_order(token, order_id)
    
    return {"success": True, "message": "Заказ оплачен!"}