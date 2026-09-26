import sqlite3

conn = sqlite3.connect("mutual_funds.db")
cursor = conn.cursor()

MIN_CAGR = -30
MAX_CAGR = 60
MIN_VOL = 0
MAX_VOL = 60

# Find scheme_codes of outlier funds
cursor.execute("""
    SELECT scheme_code, scheme_name FROM fund_metrics
    WHERE cagr < ? OR cagr > ? OR volatility < ? OR volatility > ?
""", (MIN_CAGR, MAX_CAGR, MIN_VOL, MAX_VOL))

outliers = cursor.fetchall()
print(f"Marking {len(outliers)} funds as inactive:")
for code, name in outliers:
    print(f"  {code}: {name}")
    cursor.execute("UPDATE funds SET is_active = 0 WHERE scheme_code = ?", (code,))

conn.commit()

# Verify count of remaining active funds
cursor.execute("""
    SELECT COUNT(*) FROM fund_metrics fm
    JOIN funds f ON fm.scheme_code = f.scheme_code
    WHERE f.is_active = 1
""")
print(f"\nRemaining active funds: {cursor.fetchone()[0]}")

conn.close()