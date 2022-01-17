import sqlite3
import os

databases_path = r'C:\Users\dmitriy.anurin\Documents\Projects\technical-inspection-app\databases'

users_db_path = os.path.join(databases_path, 'users.db')
users_db_connection = sqlite3.connect(users_db_path)
car_db_connection = sqlite3.connect(os.path.join(databases_path, 'cars.db'))

users_cursor = users_db_connection.cursor()
create_users_table_query = "CREATE TABLE IF NOT EXISTS users (id int, username text, car_id int)"
users_cursor.execute(create_users_table_query)
users_db_connection.commit()


cars_cursor = car_db_connection.cursor()
create_cars_table_query = "CREATE TABLE IF NOT EXISTS cars (id int, marka text, model text, year text, engine_type text, engine_value text, transmission_type text, drive_unit text)"
cars_cursor.execute(create_cars_table_query)
car_db_connection.commit()

lexus_entity = {
    'id': 1,
    'marka': 'Lexus',
    'model': 'GS300',
    'year': '2006-2010',
    'engine_type': 'Бензин',
    'engine_value': '3.0',
    'transmission_type': 'AT',
    'drive_unit': '2WD'
}

select_car_query = "SELECT * FROM cars"
result = cars_cursor.execute(select_car_query).fetchone()
if not result:
    insert_lexus = "INSERT INTO cars VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    paste_parameters = tuple(lexus_entity.values())
    cars_cursor.execute(insert_lexus, paste_parameters)
    car_db_connection.commit()

def filter_car(entity):
    filter_car = ''
    for field, value in entity.items():
        if value and not filter_car:
            filter_car += f'{field} = "{value}"'
        elif value and filter_car:
            filter_car += f' AND {field} = "{value}"'
    return filter_car


select_user_query = "SELECT * FROM users"
user_result = users_cursor.execute(select_user_query).fetchone()
if not user_result:
    insert_user_query = 'INSERT INTO users VALUES (1, "Гребеньков Александр", NULL)'
    users_cursor.execute(insert_user_query)
    users_db_connection.commit()


new_car_entity = {
    'marka': 'Lexus',
    'model': 'GS300',
    'year': '2006-2010',
    'engine_type': 'Бензин',
    'engine_value': '3.0',
    'transmission_type': 'AT',
    'drive_unit': '2WD'
}

filter_car = filter_car(new_car_entity)
select_car_query = f"SELECT id FROM cars WHERE ({filter_car})"
_id = int(cars_cursor.execute(select_car_query).fetchone()[0])
update_user_query = f'UPDATE users SET car_id = {_id} WHERE username = "Гребеньков Александр"'
users_cursor.execute(update_user_query)
users_db_connection.commit()
select_user_query = 'SELECT * FROM users'
user_result = users_cursor.execute(select_user_query).fetchone()
x = 1
