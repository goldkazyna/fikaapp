// Корзина
let cart = [];

// Добавить в корзину
function addToCart(item) {
    const existing = cart.find(i => i.id === item.id);
    if (existing) {
        existing.amount += 1;
    } else {
        cart.push({
            id: item.id,
            name: item.name,
            price: item.price,
            amount: 1
        });
    }
    updateCartBadge();
    tg.HapticFeedback.impactOccurred('light');
}

// Удалить из корзины
function removeFromCart(itemId) {
    const index = cart.findIndex(i => i.id === itemId);
    if (index > -1) {
        if (cart[index].amount > 1) {
            cart[index].amount -= 1;
        } else {
            cart.splice(index, 1);
        }
    }
    updateCartBadge();
    renderCart();
}

// Увеличить количество
function increaseAmount(itemId) {
    const item = cart.find(i => i.id === itemId);
    if (item) {
        item.amount += 1;
        updateCartBadge();
        renderCart();
    }
}

// Обновить бейдж корзины
function updateCartBadge() {
    const badge = document.getElementById('cart-badge');
    const total = cart.reduce((sum, item) => sum + item.amount, 0);
    if (total > 0) {
        badge.textContent = total;
        badge.style.display = 'flex';
    } else {
        badge.style.display = 'none';
    }
}

// Получить сумму корзины
function getCartTotal() {
    return cart.reduce((sum, item) => sum + (item.price * item.amount), 0);
}

// Отрисовать корзину
function renderCart() {
    const cartContent = document.getElementById('cart-content');
    
    if (cart.length === 0) {
        cartContent.innerHTML = '<div class="empty-cart">Корзина пуста</div>';
        return;
    }
    
    let html = '<div class="cart-items">';
    cart.forEach(item => {
        html += `
            <div class="cart-item">
                <div class="cart-item-info">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-price">${item.price} ₸</div>
                </div>
                <div class="cart-item-controls">
                    <button class="cart-btn" onclick="removeFromCart('${item.id}')">−</button>
                    <span class="cart-item-amount">${item.amount}</span>
                    <button class="cart-btn" onclick="increaseAmount('${item.id}')">+</button>
                </div>
            </div>
        `;
    });
    html += '</div>';
    
    const total = getCartTotal();
    html += `
        <div class="cart-total">
            <span>Итого</span>
            <span class="total-sum">${total} ₸</span>
        </div>
        <button class="btn-primary" onclick="showCheckout()">Оформить заказ</button>
    `;
    
    cartContent.innerHTML = html;
}

// Показать форму оформления
function showCheckout() {
    if (cart.length === 0) {
        tg.showAlert('Корзина пуста');
        return;
    }
    
    const total = getCartTotal();
    const cartContent = document.getElementById('cart-content');
    
    // Получаем данные из Telegram если есть
    const userName = tg.initDataUnsafe?.user?.first_name || '';
    
    cartContent.innerHTML = `
        <div class="checkout-form">
            <div class="form-group">
                <label>Ваше имя</label>
                <input type="text" id="checkout-name" value="${userName}" placeholder="Введите имя">
            </div>
            <div class="form-group">
                <label>Телефон</label>
                <input type="tel" id="checkout-phone" placeholder="+7 (___) ___-__-__">
            </div>
            <div class="cart-total">
                <span>К оплате</span>
                <span class="total-sum">${total} ₸</span>
            </div>
            <button class="btn-primary" onclick="submitOrder()">Оплатить ${total} ₸</button>
            <button class="btn-secondary" onclick="renderCart()">Назад к корзине</button>
        </div>
    `;
}

// Отправить заказ
async function submitOrder() {
    const name = document.getElementById('checkout-name').value.trim();
    const phone = document.getElementById('checkout-phone').value.trim();
    
    if (!name) {
        tg.showAlert('Введите имя');
        return;
    }
    
    if (!phone) {
        tg.showAlert('Введите телефон');
        return;
    }
    
    const total = getCartTotal();
    
    const cartContent = document.getElementById('cart-content');
    cartContent.innerHTML = '<div class="loading">Создание заказа...</div>';
    
    try {
        const response = await fetch('/api/takeaway/checkout', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                name: name,
                phone: phone,
                items: cart,
                total: total
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            cartContent.innerHTML = `<div class="error">${data.error}</div>`;
            return;
        }
        
        // Очищаем корзину
        cart = [];
        updateCartBadge();
        
        // Переходим на оплату
        window.location.href = data.payment_url;
        
    } catch (err) {
        cartContent.innerHTML = '<div class="error">Ошибка оформления заказа</div>';
    }
}

// Загрузка меню для самовывоза (с кнопками добавления)
async function loadTakeawayMenu() {
    const menuContent = document.getElementById('takeaway-menu-content');
    menuContent.innerHTML = '<div class="loading">Загрузка меню...</div>';
    
    try {
        const response = await fetch('/api/menu');
        const data = await response.json();
        
        if (!data.categories || data.categories.length === 0) {
            menuContent.innerHTML = '<div class="error">Меню пока пустое</div>';
            return;
        }
        
        let html = '';
        data.categories.forEach((category, index) => {
            const isOpen = index === 0;
            
            html += `<div class="category ${isOpen ? 'open' : ''}">`;
            html += `
                <div class="category-header" onclick="toggleCategory(this)">
                    <span class="category-title">${category.name}</span>
                    <span class="category-count">${category.items.length}</span>
                    <span class="category-arrow">›</span>
                </div>
            `;
            html += `<div class="category-items">`;
            
            category.items.forEach(item => {
                const imageHtml = item.image 
                    ? `<img class="dish-image" src="${item.image}" alt="${item.name}">`
                    : `<div class="dish-image no-image">🍽</div>`;
                
                const itemData = JSON.stringify({
                    id: item.id,
                    name: item.name,
                    price: item.price
                }).replace(/"/g, '&quot;');
                
                html += `
                    <div class="dish-card">
                        ${imageHtml}
                        <div class="dish-info">
                            <div class="dish-name">${item.name}</div>
                            ${item.description ? `<div class="dish-description">${item.description}</div>` : ''}
                            <div class="dish-price">${item.price} ₸</div>
                        </div>
                        <button class="add-to-cart-btn" onclick='addToCart(${itemData})'>+</button>
                    </div>
                `;
            });
            
            html += `</div></div>`;
        });
        
        menuContent.innerHTML = html;
        
    } catch (err) {
        menuContent.innerHTML = '<div class="error">Ошибка загрузки меню</div>';
    }
}