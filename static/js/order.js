// Загрузка заказа
async function loadOrder() {
    const orderContent = document.getElementById('order-content');
    orderContent.innerHTML = '<div class="loading">Загрузка заказа...</div>';
    
    try {
        const response = await fetch('/api/order/' + tableNum);
        const data = await response.json();
        
        if (data.error) {
            orderContent.innerHTML = '<div class="error">' + data.error + '</div>';
            return;
        }
        
        let html = '<div class="menu-list">';
        data.items.forEach(item => {
            html += `
                <div class="order-item">
                    <span class="item-name">${item.name}</span>
                    <span class="item-price">${item.price} ₸</span>
                </div>
            `;
        });
        html += '</div>';
        
        html += `
            <div class="order-total">
                <span>Итого</span>
                <span class="total-sum">${data.total} ₸</span>
            </div>
            <button class="btn-primary" id="btn-pay-now">Оплатить ${data.total} ₸</button>
        `;
        
        orderContent.innerHTML = html;
        document.getElementById('btn-pay-now').onclick = payOrder;
        
    } catch (err) {
        orderContent.innerHTML = '<div class="error">Ошибка загрузки</div>';
    }
}

// Оплата заказа
async function payOrder() {
    const btn = document.getElementById('btn-pay-now');
    btn.disabled = true;
    btn.textContent = 'Создание платежа...';
    
    try {
        const response = await fetch('/api/pay/' + tableNum, {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.error) {
            document.getElementById('order-content').innerHTML = '<div class="error">' + data.error + '</div>';
            return;
        }
        
        window.location.href = data.payment_url;
        
    } catch (err) {
        document.getElementById('order-content').innerHTML = '<div class="error">Ошибка создания платежа</div>';
    }
}