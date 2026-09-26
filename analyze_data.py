import sqlite3
import statistics
import math
from datetime import datetime

conn = sqlite3.connect("mutual_funds.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM fund_metrics")

cursor.execute("""
    SELECT 
        f.scheme_code, f.category, f.scheme_name,
        MIN(n.nav_date) as start_date,
        MAX(n.nav_date) as end_date
    FROM funds f
    JOIN nav_history n ON f.scheme_code = n.scheme_code
    GROUP BY f.scheme_code
""")
fund_ranges = cursor.fetchall()

print(f"Processing {len(fund_ranges)} funds...\n")

processed = 0
skipped = []

for scheme_code, category, name, start_date, end_date in fund_ranges:
    cursor.execute("SELECT nav_value FROM nav_history WHERE scheme_code = ? AND nav_date = ?", (scheme_code, start_date))
    result = cursor.fetchone()
    if result is None or result[0] == 0:
        skipped.append((name, "invalid/zero start NAV"))
        continue
    start_nav = result[0]

    cursor.execute("SELECT nav_value FROM nav_history WHERE scheme_code = ? AND nav_date = ?", (scheme_code, end_date))
    result = cursor.fetchone()
    if result is None or result[0] == 0:
        skipped.append((name, "invalid/zero end NAV"))
        continue
    end_nav = result[0]

    d1 = datetime.strptime(start_date, "%Y-%m-%d")
    d2 = datetime.strptime(end_date, "%Y-%m-%d")
    years = (d2 - d1).days / 365.25
    if years <= 0:
        skipped.append((name, "zero/negative time span"))
        continue
    cagr = ((end_nav / start_nav) ** (1 / years) - 1) * 100

    cursor.execute("SELECT nav_value FROM nav_history WHERE scheme_code = ? ORDER BY nav_date ASC", (scheme_code,))
    nav_values = [row[0] for row in cursor.fetchall() if row[0] > 0]  # also filter zero NAVs here
    if len(nav_values) < 2:
        skipped.append((name, "not enough valid NAV points"))
        continue

    daily_returns = [(nav_values[i] - nav_values[i-1]) / nav_values[i-1] for i in range(1, len(nav_values))]
    volatility = statistics.stdev(daily_returns) * math.sqrt(252) * 100 if len(daily_returns) > 1 else None

    cursor.execute("""
        INSERT INTO fund_metrics (scheme_code, category, scheme_name, years_of_data, cagr, volatility)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (scheme_code, category, name, round(years, 2), cagr, volatility))

    processed += 1

conn.commit()
conn.close()

print(f"Successfully processed: {processed}")
print(f"Skipped: {len(skipped)}")
if skipped:
    print("\nSkipped funds and reasons:")
    for name, reason in skipped:
        print(f"  {name}: {reason}")