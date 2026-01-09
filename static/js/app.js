const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

// Настройки Telegram WebApp
tg.setHeaderColor('#1c1c1d');
tg.setBackgroundColor('#1c1c1d');

// Получаем номер стола
let tableNum = '65';

const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get('table')) {
    tableNum = urlParams.get('table');
}

const startParam = tg.initDataUnsafe?.start_param;
if (startParam && startParam.startsWith('table_')) {
    tableNum = startParam.replace('table_', '');
}

// Заполняем данные
document.getElementById('username').textContent = 
    tg.initDataUnsafe?.user?.first_name || 'гость';
document.getElementById('table-num').textContent = tableNum;

// Навигация
const pages = {
    main: document.getElementById('main-page'),
    menu: document.getElementById('menu-page'),
    order: document.getElementById('order-page'),
    takeaway: document.getElementById('takeaway-page'),
    cart: document.getElementById('cart-page')
};

function showPage(pageName) {
    Object.values(pages).forEach(page => page.classList.remove('active'));
    pages[pageName].classList.add('active');
}

// Кнопки главной страницы
document.getElementById('btn-menu').onclick = async function() {
    showPage('menu');
    await loadMenu();
};

document.getElementById('btn-takeaway').onclick = async function() {
    showPage('takeaway');
    await loadTakeawayMenu();
};

document.getElementById('btn-bonus').onclick = function() {
    tg.showAlert('Бонусная программа — скоро будет!');
};

document.getElementById('btn-pay').onclick = async function() {
    showPage('order');
    await loadOrder();
};

// Кнопки назад
document.getElementById('menu-back').onclick = function() {
    showPage('main');
};

document.getElementById('order-back').onclick = function() {
    showPage('main');
};

document.getElementById('takeaway-back').onclick = function() {
    showPage('main');
};

document.getElementById('cart-back').onclick = function() {
    showPage('takeaway');
};

// Кнопка корзины
document.getElementById('btn-cart').onclick = function() {
    showPage('cart');
    renderCart();
};