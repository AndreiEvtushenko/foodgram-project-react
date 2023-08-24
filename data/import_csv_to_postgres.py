import csv
import psycopg2

# Параметры подключения к базе данных PostgreSQL
db_params = {
    'dbname': 'django',
    'user': 'django_user',
    'password': 'mysecretpassword',
    'host': '172.24.0.3',
    'port': '5432',
}

# Подключаемся к базе данных PostgreSQL
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

csv_file = 'ingredients.csv'
with open(csv_file, 'r', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)  # Пропускаем заголовок, если он есть в CSV файле
    for row in csv_reader:
        # Вставляем данные в таблицу
        cursor.execute('INSERT INTO foodgram_ingredient (name, measurement_unit) VALUES (%s, %s)', (row[0], row[1]))

# Сохраняем изменения и закрываем соединение с базой данных
conn.commit()
conn.close()
