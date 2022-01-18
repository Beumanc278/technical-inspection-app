def create_filter(parameters: dict) -> str:
    where_query_part = ''
    for field, value in parameters.items():
        if value and not where_query_part:
            paste_value = f'"{value}"' if isinstance(value, str) else f'{value}'
            where_query_part += f'"{field}" = {paste_value}'
        elif value and where_query_part:
            paste_value = f'"{value}"' if isinstance(value, str) else f'{value}'
            where_query_part += f' AND "{field}" = {paste_value}'
    return where_query_part