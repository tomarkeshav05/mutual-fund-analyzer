import requests

response = requests.get("https://api.mfapi.in/mf/119551")
data = response.json()

print(data['meta'])  # fund info
print(data['data'][:5])  # first 5 NAV entries

import requests

scheme_codes = {
    "large_cap": 118269,
    "small_cap": 118525,
    "debt": 120256,
    "hybrid": 118272,
    "index": 118266
}

all_fund_data = {}

for category, code in scheme_codes.items():
    response = requests.get(f"https://api.mfapi.in/mf/{code}")
    data = response.json()
    all_fund_data[category] = data
    print(f"--- {category.upper()} ---")
    print(data['meta']['scheme_name'])
    print("Number of NAV records:", len(data['data']))
    print()

    print("=" * 40)
print("DETAILED CHECK")
print("=" * 40)

for category, data in all_fund_data.items():
    nav_list = data['data']
    print(f"\n{category.upper()} - {data['meta']['scheme_name']}")
    print("Oldest record:", nav_list[-1])
    print("Newest record:", nav_list[0])
    print("Total records:", len(nav_list))