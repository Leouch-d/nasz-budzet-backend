import sqlite3
import os
import sys
DB_FILE = 'budzet.db'
if not os.path.exists(DB_FILE):
    print(f"BŁĄD: Nie znaleziono pliku bazy danych '{DB_FILE}'", file=sys.stderr)
    exit(1)
try:
    con = sqlite3.connect(DB_FILE)
    for line in con.iterdump():
        print(line)
    con.close()
except Exception as e:
    print(f"BŁĄD: Wystąpił problem podczas próby zrzutu bazy danych: {e}", file=sys.stderr)
    exit(1)
