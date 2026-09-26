import sqlite3

conn = sqlite3.connect("mutual_funds.db")
cursor = conn.cursor()

# Delete the old broken debt fund entry
cursor.execute("DELETE FROM funds WHERE scheme_code = 116022")

conn.commit()

# Verify only one debt fund remains
cursor.execute("SELECT scheme_code, scheme_name, category FROM funds WHERE category = 'debt'")
print("Remaining debt fund(s):")
for row in cursor.fetchall():
    print(row)

conn.close()