import csv
import psycopg2

db_params = {
    'dbname': 'django',
    'user': 'django_user',
    'password': 'mysecretpassword',
    'host': '172.23.0.2',
    'port': '5432',
}

conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

csv_file = 'ingredients.csv'
with open(csv_file, 'r', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)
    for row in csv_reader:
        cursor.execute('INSERT INTO foodgram_ingredient (name, measurement_unit) VALUES (%s, %s)', (row[0], row[1]))

conn.commit()
conn.close()
