import sqlite3
import csv

conn = sqlite3.connect('/user/dev/copy_foodgram/foodgram-project-react/backend/db.sqlite3')
cursor = conn.cursor()

csv_file = 'ingredients.csv'
with open(csv_file, 'r', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)
    for row in csv_reader:
        cursor.execute('INSERT INTO foodgram_ingredient (name, measurement_unit) VALUES (?, ?)', (row[0], row[1]))

conn.commit()
conn.close()
