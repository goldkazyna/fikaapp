from fastapi import APIRouter
from iiko.menu import get_menu

router = APIRouter(prefix="/api")


@router.get("/menu")
async def menu():
    """Получить меню"""
    return get_menu()