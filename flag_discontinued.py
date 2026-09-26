import sqlite3

conn = sqlite3.connect("mutual_funds.db")
cursor = conn.cursor()

cursor.execute("""
    UPDATE funds 
    SET is_active = 0 
    WHERE scheme_name LIKE '%Tata Corporate Bond%'
""")

conn.commit()

# Verify
cursor.execute("SELECT scheme_code, scheme_name, is_active FROM funds WHERE is_active = 0")
print("Inactive/discontinued funds:")
for row in cursor.fetchall():
    print(row)

conn.close()