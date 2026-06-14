async def normalize_query_params(items: list) -> dict:
    """Функция нормализации параметров запроса"""
    normalized: dict = {}
    for key, value in items:
        clean_key = key.strip() if key else ""
        if not clean_key:
            continue
        clean_value = value.strip() if value else ""
        existing = normalized.get(clean_key)
        if existing is None:
            normalized[clean_key] = clean_value
        elif isinstance(existing, list):
            existing.append(clean_value)
        else:
            normalized[clean_key] = [existing, clean_value]
    return normalized
