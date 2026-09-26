import requests
import sqlite3
import json
import time

with open("selected_funds.json", "r") as f:
    selected_funds = json.load(f)

conn = sqlite3.connect("mutual_funds.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM nav_history")
cursor.execute("DELETE FROM funds")

total = len(selected_funds)
loaded_count = 0
failed = []

for i, (key, info) in enumerate(selected_funds.items(), 1):
    code = info['code']
    category = info['category']

    try:
        response = requests.get(f"https://api.mfapi.in/mf/{code}", timeout=10)
        data = response.json()

        meta = data['meta']
        nav_list = data['data']

        cursor.execute("""
            INSERT OR REPLACE INTO funds (scheme_code, scheme_name, category, fund_house)
            VALUES (?, ?, ?, ?)
        """, (code, meta['scheme_name'], category, meta['fund_house']))

        count_inserted = 0
        for entry in nav_list:
            try:
                day, month, year = entry['date'].split('-')
                proper_date = f"{year}-{month}-{day}"
                nav_value = float(entry['nav'])
                cursor.execute("""
                    INSERT INTO nav_history (scheme_code, nav_date, nav_value)
                    VALUES (?, ?, ?)
                """, (code, proper_date, nav_value))
                count_inserted += 1
            except (ValueError, KeyError):
                continue

        loaded_count += 1
        print(f"[{i}/{total}] Loaded {category} ({code}): {count_inserted} records")

    except Exception as e:
        failed.append((code, category, str(e)))
        print(f"[{i}/{total}] FAILED {category} ({code}): {e}")

    time.sleep(0.1)  # small delay to be polite to the free API

conn.commit()
conn.close()

print(f"\n=== DONE: {loaded_count}/{total} funds loaded successfully ===")
if failed:
    print(f"\n{len(failed)} funds failed:")
    for code, cat, err in failed:
        print(f"  {cat} ({code}): {err}")