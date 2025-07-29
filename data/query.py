import sqlite3
DB_PATH = 'data.db'
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""EXPLAIN QUERY PLAN
SELECT password FROM fullPairings WHERE prefix = '5baa6' AND hash = '5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8';""")
results = cursor.fetchall()
print(results)

cursor.close()
conn.close()