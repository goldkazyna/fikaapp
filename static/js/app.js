const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

// Получаем номер стола из параметра
const urlParams = new URLSearchParams(window.location.search);
const tableNum = urlParams.get('table') || '65';

// Заполняем данные
document.getElementById('username').textContent = 
    tg.initDataUnsafe?.user?.first_name || 'гость';
document.getElementById('table-num').textContent = tableNum;

const modal = document.getElementById('modal');
const orderContent = document.getElementById('order-content');

let currentOrderTotal = 0;

// Кнопка Меню
document.getElementById('btn-menu').onclick = function() {
    tg.showAlert('Меню — скоро будет!');
};

// Кнопка С собой
document.getElementById('btn-takeaway').onclick = function() {
    tg.showAlert('С собой — скоро будет!');
};

// Кнопка Оплатить - открывает модалку
document.getElementById('btn-pay').onclick = async function() {
    modal.classList.add('active');
    await loadOrder();
};

// Закрыть модалку
document.getElementById('modal-close').onclick = function() {
    modal.classList.remove('active');
};

// Загрузка заказа
async function loadOrder() {
    orderContent.innerHTML = '<div class="loading">Загрузка заказа...</div>';
    
    try {
        const response = await fetch('/api/order/' + tableNum);
        const data = await response.json();
        
        if (data.error) {
            orderContent.innerHTML = '<div class="error">' + data.error + '</div>';
            return;
        }
        
        currentOrderTotal = data.total;
        
        let html = '';
        data.items.forEach(item => {
            html += `
                <div class="order-item">
                    <span class="item-name">${item.name}</span>
                    <span class="item-price">${item.price} ₸</span>
                </div>
            `;
        });
        
        html += `
            <div class="order-total">
                <span>Итого:</span>
                <span class="total-sum">${data.total} ₸</span>
            </div>
            <button class="btn-pay-now" id="btn-pay-now">Оплатить ${data.total} ₸</button>
        `;
        
        orderContent.innerHTML = html;
        
        // Привязываем обработчик к кнопке оплаты
        document.getElementById('btn-pay-now').onclick = payOrder;
        
    } catch (err) {
        orderContent.innerHTML = '<div class="error">Ошибка загрузки</div>';
    }
}

// Оплата заказа
async function payOrder() {
    const btn = document.getElementById('btn-pay-now');
    btn.disabled = true;
    btn.textContent = 'Оплата...';
    
    try {
        const response = await fetch('/api/pay/' + tableNum, {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.error) {
            orderContent.innerHTML = '<div class="error">' + data.error + '</div>';
            return;
        }
        
        orderContent.innerHTML = '<div class="success">✅ Оплачено!</div>';
        
        // Закрываем через 2 секунды
        setTimeout(() => {
            modal.classList.remove('active');
            tg.showAlert('Спасибо! Заказ оплачен.');
        }, 2000);
        
    } catch (err) {
        orderContent.innerHTML = '<div class="error">Ошибка оплаты</div>';
    }
}