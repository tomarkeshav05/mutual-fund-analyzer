import sqlite3

conn = sqlite3.connect("mutual_funds.db")
cursor = conn.cursor()

# Realistic bounds for Indian mutual funds (generous, but excludes impossible values)
MIN_CAGR = -30   # even a bad fund rarely loses more than this annually over its full history
MAX_CAGR = 60    # even top small-caps/silver rarely sustain more than this long-term
MIN_VOL = 0
MAX_VOL = 60     # even the most volatile equity/silver funds rarely exceed this annualized

cursor.execute("""
    SELECT scheme_code, scheme_name, category, cagr, volatility 
    FROM fund_metrics
    WHERE cagr < ? OR cagr > ? OR volatility < ? OR volatility > ?
""", (MIN_CAGR, MAX_CAGR, MIN_VOL, MAX_VOL))

outliers = cursor.fetchall()

print(f"Found {len(outliers)} outlier funds:\n")
for code, name, category, cagr, vol in outliers:
    print(f"{category:15} | CAGR: {cagr:8.2f}% | Vol: {vol:8.2f}% | {name}")

conn.close()