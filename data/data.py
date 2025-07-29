from hashlib import sha1
import sqlite3
import os

'''
Creates sqlite database from SecList Passwords folder 
to enable rainbow table attack on SHA1 prefixes.

https://github.com/danielmiessler/SecLists/tree/master/Passwords
'''

def createHashTable():
   cursor.execute("""CREATE TABLE IF NOT EXISTS hashPairs(
                  sha1 TEXT,
                  password TEXT
               );""")

def insertHashTableDataFromPath():
   # Relatice path to downloaded SecList folders
   PATH = 'Passwords/Leaked-Databases'
   for root, _, files in os.walk(PATH):
      for file in files:
         file_path = os.path.join(root, file)
         try:
            with open(file_path, 'r') as lines:
               for line in lines:
                  password = line.strip()
                  if password:
                     if 'Floating-comp' in file_path:
                        sha1_hash = sha1(password.split(':')[0].encode('utf-8')).hexdigest()
                     else:
                        sha1_hash = sha1(password.encode('utf-8')).hexdigest()
                     try:
                        cursor.execute("""INSERT OR IGNORE INTO hashPairs (sha1, password) VALUES (?, ?);""", (sha1_hash, password))
                     except Exception as e:
                           print(f"Error inserting {password} into database:", e)
                  else:
                     continue
         except Exception as e:
            print(f"Failed to read {file_path}: {e}")

   conn.commit()

def insertHashTableDataFromFile():
   # Relative path to downloaded SecList files
   FILE_PATH = 'Passwords/unknown-azul.txt'
   try:
      with open(FILE_PATH, 'r') as lines:
         for line in lines:
            password = line.strip()
            if password:
               if 'Floating-comp' in FILE_PATH:
                  sha1_hash = sha1(password.split(':')[0].encode('utf-8')).hexdigest()
               else:
                  sha1_hash = sha1(password.encode('utf-8')).hexdigest()
               try:
                  cursor.execute("""INSERT OR IGNORE INTO hashPairs (sha1, password) VALUES (?, ?);""", (sha1_hash, password))
               except Exception as e:
                     print(f"Error inserting {password} into database:", e)
            else:
               continue
   except Exception as e:
      print(f"Failed to read {FILE_PATH}: {e}")

def createPrefixesTable():
   cursor.execute("""CREATE TABLE IF NOT EXISTS prefixes(
                  prefix TEXT PRIMARY KEY
               );""")
   conn.commit()

def createPlaintextTable():
   cursor.execute("""PRAGMA foreign_keys = ON;""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS plaintexts(
               prefix TEXT,
               plaintext TEXT,
               FOREIGN KEY (prefix) REFERENCES prefixes(prefix)
            );""")
   conn.commit()

# Because I stupidly dropped the original hash table...
def createFullPairingsTable():
   cursor.execute("""PRAGMA foreign_keys = ON;""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS fullPairings(
                  prefix TEXT,
                  password TEXT,
                  hash TEXT,
                  FOREIGN KEY (prefix) REFERENCES prefixes(prefix)
                  );""")
   conn.commit()

# Sort data according to prefixes for faster lookup
def sortPrefixes():
   cursor.execute("""INSERT OR IGNORE INTO prefixes (prefix)
                     SELECT SUBSTR(sha1, 1, 5)
                     FROM hashPairs
               """)
   conn.commit()
   
   cursor.execute("""INSERT OR IGNORE INTO plaintexts (prefix, plaintext)
                  SELECT SUBSTR(sha1, 1, 5), password
                  FROM hashPairs
            """)
   conn.commit()

def insertHashPrefixPlaintext():
   cursor.execute(""" SELECT prefix, plaintext 
                  FROM plaintexts
                  """)
   
   for prefix, plaintext in cursor.fetchall():
      sha1_hash = sha1(plaintext.encode('utf-8')).hexdigest()
      cursor.execute(""" INSERT OR IGNORE INTO fullPairings (prefix, password, hash) VALUES (?, ?, ?);""", (prefix, plaintext, sha1_hash))
   
   conn.commit()


def createIndex():
   cursor.execute("""CREATE INDEX IF NOT EXISTS idx_prefix ON fullPairings(prefix);""")
   conn.commit()

   cursor.execute("""CREATE INDEX IF NOT EXISTS idx_prefix_hash ON fullPairings(prefix, hash);""")
   conn.commit()
   

if __name__ == '__main__':
   DB_PATH = 'data.db'

   conn = sqlite3.connect(DB_PATH)
   cursor = conn.cursor()

   cursor.execute("BEGIN TRANSACTION;")
   # Call SQLite query functions here

   cursor.close()
   conn.close()