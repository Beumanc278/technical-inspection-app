def create_filter(parameters: dict) -> str:
    where_query_part = ''
    for field, value in parameters.items():
        if value and not where_query_part:
            where_query_part += f'"{field}" = "{value}"'
        elif value and where_query_part:
            where_query_part += f' AND "{field}" = "{value}"'
    return where_query_part