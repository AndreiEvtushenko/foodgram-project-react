import sqlite3
import csv

# Подключаемся к существующей базе данных SQLite3
conn = sqlite3.connect('/user/dev/copy_foodgram/foodgram-project-react/backend/db.sqlite3')
cursor = conn.cursor()

# Открываем CSV файл и выполняем импорт данных в таблицу базы данных
csv_file = 'ingredients.csv'
with open(csv_file, 'r', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)  # Пропускаем заголовок, если он есть в CSV файле
    for row in csv_reader:
        # Вставляем данные в таблицу, пропустив первый столбец (id), так как id будет генерироваться автоматически
        cursor.execute('INSERT INTO foodgram_ingredient (name, measurement_unit) VALUES (?, ?)', (row[0], row[1]))

# Сохраняем изменения и закрываем соединение с базой данных
conn.commit()
conn.close()
