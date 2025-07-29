import sqlite3

'''
Remove uncessary tables from 'data.db'
'''

if __name__ == '__main__':
   DB_PATH = 'data_xs.db'

   conn = sqlite3.connect(DB_PATH)
   cursor = conn.cursor()

   cursor.execute("BEGIN TRANSACTION;")
   # Call SQLite query functions here
   cursor.execute("""DROP TABLE plaintexts""")

   cursor.close()
   conn.close()