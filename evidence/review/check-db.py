import sqlite3
import json

db = sqlite3.connect('data/auditoria.db')
cursor = db.cursor()

# Get tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cursor.fetchall()]

print(f'Tables: {len(tables)}')
for table in tables:
    print(f'  - {table}')

print()
print('Row counts:')
for table in tables:
    cursor.execute(f'SELECT COUNT(*) FROM {table}')
    count = cursor.fetchone()[0]
    print(f'  {table}: {count} rows')

# Get schema
print()
print('Schema:')
for table in tables:
    cursor.execute(f'PRAGMA table_info({table})')
    columns = cursor.fetchall()
    print(f'  {table}:')
    for col in columns:
        print(f'    - {col[1]} ({col[2]})')

db.close()
