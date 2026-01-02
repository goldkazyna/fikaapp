# Маппинг номер стола -> table_id
TABLES = {
    "11": "8d4fb7e4-8516-4c06-b6ba-6c79fab570a5",
    "31": "f4daf69c-0e66-45bb-b138-b7bf804dca44",
    "65": "b76f1f9d-55f4-4380-843c-821a1d09c41a",
}


def get_table_id(table_num: str):
    """Получить ID стола по номеру"""
    return TABLES.get(table_num)