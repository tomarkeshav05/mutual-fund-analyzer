import sqlite3
conn = sqlite3.connect("mutual_funds.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT nav_date, nav_value FROM nav_history
    WHERE scheme_code = (SELECT scheme_code FROM funds WHERE scheme_name LIKE '%Tata Corporate Bond%')
    ORDER BY nav_date ASC
    LIMIT 10
""")
print("First 10 records:")
for row in cursor.fetchall():
    print(row)

cursor.execute("""
    SELECT nav_date, nav_value FROM nav_history
    WHERE scheme_code = (SELECT scheme_code FROM funds WHERE scheme_name LIKE '%Tata Corporate Bond%')
    ORDER BY nav_date DESC
    LIMIT 10
""")
print("\nLast 10 records:")
for row in cursor.fetchall():
    print(row)

conn.close()