from fastapi import APIRouter, Request
from database.models import get_payment, update_payment_status
from iiko.api import get_token, add_payment as iiko_add_payment, close_order

router = APIRouter(prefix="/api")


@router.post("/webhook/plexy")
async def plexy_webhook(request: Request):
    """Webhook от Plexy — оплата прошла"""
    data = await request.json()
    
    print("📩 Webhook от Plexy:", data)
    
    event_name = data.get("name", "")
    event_data = data.get("data", {})
    
    # Получаем payment_id из разных форматов
    payment_link_id = event_data.get("paymentLinkId")
    if isinstance(payment_link_id, dict):
        payment_id = payment_link_id.get("Value")
    else:
        payment_id = payment_link_id
    
    status = event_data.get("status")
    
    print(f"📋 Event: {event_name}, Status: {status}, Payment ID: {payment_id}")
    
    if not payment_id:
        return {"error": "No payment_id"}
    
    # Получаем платёж из базы
    payment = get_payment(payment_id)
    
    if not payment:
        print(f"❌ Платёж не найден: {payment_id}")
        return {"error": "Payment not found"}
    
    # Если уже оплачен — пропускаем
    if payment["status"] == "paid":
        print("⏭ Уже оплачен, пропускаем")
        return {"success": True}
    
    # Если оплата успешна (authorized или captured)
    if status in ["authorized", "captured", "successful", "completed", "paid"]:
        # Обновляем статус в базе
        update_payment_status(payment_id, "paid")
        
        # Закрываем заказ в iiko
        token = get_token()
        order_id = payment["order_id"]
        amount = payment["amount"]
        
        iiko_add_payment(token, order_id, amount)
        close_order(token, order_id)
        
        print(f"✅ Заказ {order_id} закрыт!")
    
    return {"success": True}