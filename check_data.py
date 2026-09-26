import sqlite3

conn = sqlite3.connect("mutual_funds.db")
cursor = conn.cursor()

print("=== FUNDS TABLE (grouped by category) ===")
cursor.execute("SELECT category, COUNT(*) FROM funds GROUP BY category")
for row in cursor.fetchall():
    print(row)

print("\n=== ALL FUNDS ===")
cursor.execute("SELECT scheme_code, scheme_name, category FROM funds ORDER BY category")
for row in cursor.fetchall():
    print(row)

print("\n=== NAV RECORD COUNT PER FUND ===")
cursor.execute("""
    SELECT f.category, f.scheme_name, COUNT(n.id) as record_count
    FROM funds f
    JOIN nav_history n ON f.scheme_code = n.scheme_code
    GROUP BY f.scheme_code
    ORDER BY f.category
""")
for row in cursor.fetchall():
    print(row)

conn.close()