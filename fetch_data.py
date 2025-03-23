import sqlite3
import json

conn = sqlite3.connect("knowledge_base.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM rules")
rows = cursor.fetchall()

for row in rows:
    print(f"Job Role: {row[1]}")
    print(f"Must-Have Skills: {json.loads(row[2])}")
    print(f"Nice-To-Have Skills: {json.loads(row[3])}")
    print(f"GPA Cutoff: {row[4]}")
    print(f"Minimum Experience: {row[5]}")
    print("-" * 40)

conn.close()