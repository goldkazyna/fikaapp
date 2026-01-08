// Загрузка меню
async function loadMenu() {
    const menuContent = document.getElementById('menu-content');
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
                
                html += `
                    <div class="dish-card">
                        ${imageHtml}
                        <div class="dish-info">
                            <div class="dish-name">${item.name}</div>
                            ${item.description ? `<div class="dish-description">${item.description}</div>` : ''}
                            <div class="dish-price">${item.price} ₸</div>
                        </div>
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

// Переключение категории
function toggleCategory(header) {
    const category = header.parentElement;
    category.classList.toggle('open');
}