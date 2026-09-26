import requests
import json
import re

response = requests.get("https://api.mfapi.in/mf")
all_schemes = response.json()

print("Total schemes available:", len(all_schemes))

# Expanded categories including gold, silver, international, sector funds
categories = {
    "large_cap": ["large cap"],
    "mid_cap": ["mid cap"],
    "small_cap": ["small cap"],
    "debt": ["corporate bond", "banking and psu", "short term debt", "medium duration"],
    "hybrid": ["hybrid", "balanced advantage"],
    "index": ["nifty 50 index", "sensex index"],
    "elss": ["elss", "tax saver"],
    "gold": ["gold fund", "gold etf"],
    "silver": ["silver fund", "silver etf"],
    "international": ["international", "global", "us equity", "nasdaq"],
    "banking_sector": ["banking fund", "banking and financial"],
    "pharma_sector": ["pharma", "healthcare fund"],
    "technology_sector": ["technology fund", "digital fund"],
}

matched_funds = {cat: [] for cat in categories}

for scheme in all_schemes:
    name = scheme['schemeName'].lower()
    if "direct" not in name or "growth" not in name:
        continue
    if "idcw" in name or "dividend" in name:
        continue
    for cat, keywords in categories.items():
        if any(kw in name for kw in keywords):
            matched_funds[cat].append(scheme)
            break

# Auto-pick up to 20 funds per category (adjust per category based on availability)
selected = {}
for cat, funds in matched_funds.items():
    picks = funds[:20]  # take first 20 matches per category
    print(f"{cat}: {len(funds)} found, picking {len(picks)}")
    for f in picks:
        key = f"{cat}_{f['schemeCode']}"
        selected[key] = {"code": f['schemeCode'], "category": cat, "name": f['schemeName']}

print(f"\nTotal funds selected: {len(selected)}")

# Save to a JSON file so load_data.py can use it directly
with open("selected_funds.json", "w") as f:
    json.dump(selected, f, indent=2)

print("Saved to selected_funds.json")