import sqlite3


def get_all_data():
    with sqlite3.connect('sensors_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sensor_data')
        rows = cursor.fetchall()
        return rows


# Получение всех данных
all_data = get_all_data()
for row in all_data:
    print(row)
