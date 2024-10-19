import sqlite3

# Подключение к базе данных (если базы нет, она будет создана)
conn = sqlite3.connect('sensors_data.db')
cursor = conn.cursor()

# Создание таблицы, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pressure INTEGER,
    co2eq INTEGER,
    humidity INTEGER,
    co2 INTEGER,
    tvoc INTEGER,
    temperature INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Сохраняем изменения
conn.commit()
