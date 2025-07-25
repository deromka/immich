import requests

API_URL = "http://192.168.2.54:2283/api/search/metadata"
API_KEY = "LMaVxA03VIxImcV2mhMSGVFEmQxpA4cagRmPjw0V35Q"

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

# Filter assets by filename containing "-thumbnail.webp"
payload = {
    "originalFileName": "-thumbnail.webp",
    "withDeleted": False,
    "size": 1000,
    "page": 1
}

response = requests.post(API_URL, json=payload, headers=headers)

try:
    data = response.json()
except Exception as e:
    print("❌ JSON decode error:", e)
    print("Raw response:", response.text)
    exit(1)

if response.status_code != 200:
    print(f"❌ Error {response.status_code}: {data.get('message', '')}")
    print(data)
    exit(1)

# Correctly access nested structure
assets = data.get("assets", {}).get("items", [])

print(f"✅ Found {len(assets)} thumbnail assets:")
for asset in assets:
    print(f"{asset['id']} | {asset['originalFileName']} | {asset.get('originalPath', '')}")

