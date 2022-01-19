def create_filter(parameters: dict, operation: str = "SELECT") -> str:
    if operation == "SELECT":
        divide_symbol = " AND"
    elif operation == "UPDATE":
        divide_symbol = ", "
    where_query_part = ''
    for field, value in parameters.items():
        if value not in [None, [], 0] and not where_query_part:
            paste_value = f'"{value}"' if isinstance(value, str) else f'{value}'
            where_query_part += f'"{field}" = {paste_value}'
        elif value not in [None, [], 0] and where_query_part:
            paste_value = f'"{value}"' if isinstance(value, str) else f'{value}'
            where_query_part += f'{divide_symbol} "{field}" = {paste_value}'
    return where_query_part