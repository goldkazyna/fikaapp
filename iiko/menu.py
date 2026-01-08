import requests
from config import API_KEY, ORG_ID, IIKO_API_URL


MENU_ID = "69654"


def get_token():
    response = requests.post(
        f"{IIKO_API_URL}/access_token",
        json={"apiLogin": API_KEY}
    )
    return response.json()["token"]


def get_menu():
    """Получить меню из iiko"""
    token = get_token()
    
    response = requests.post(
        "https://api-ru.iiko.services/api/2/menu/by_id",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "organizationIds": [ORG_ID],
            "externalMenuId": MENU_ID
        }
    )
    
    if response.status_code != 200:
        return {"categories": []}
    
    data = response.json()
    
    # Форматируем для фронтенда
    categories = []
    for cat in data.get("itemCategories", []):
        items = []
        for item in cat.get("items", []):
            # Получаем цену и фото из itemSizes
            price = 0
            image = None
            sizes = item.get("itemSizes", [])
            
            if sizes:
                prices = sizes[0].get("prices", [])
                if prices:
                    price = prices[0].get("price", 0)
                image = sizes[0].get("buttonImageUrl")
            
            items.append({
                "id": item.get("itemId"),
                "name": item.get("name"),
                "description": item.get("description", ""),
                "price": price,
                "image": image
            })
        
        if items:
            categories.append({
                "id": cat.get("id"),
                "name": cat.get("name"),
                "items": items
            })
    
    return {"categories": categories}