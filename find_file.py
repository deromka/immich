import requests
import json

IMMICH_API_URL = "http://192.168.2.54:2283/api"
API_KEY = "LMaVxA03VIxImcV2mhMSGVFEmQxpA4cagRmPjw0V35Q"
TARGET_FILENAME = "3820acc1-f497-401f-88db-4e2258402e5c-preview.jpeg"

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "x-api-key": API_KEY,
}

def search_by_filename(filename):
    url = f"{IMMICH_API_URL}/search/metadata"
    body = {
        "originalFileName": filename,
        "size": 1,
        "page": 1
    }
    print(f"🔍 Sending POST to {url}")
    print(f"📤 Request body: {json.dumps(body)}")
    response = requests.post(url, headers=HEADERS, json=body)
    print(f"📥 Status: {response.status_code}")
    try:
        result = response.json()
        print(f"📦 Response: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"⚠ Failed to parse response: {e}")
        print(response.text)
        return None

    items = result.get("assets", {}).get("items", [])
    if items:
        asset = items[0]
        print(f"✅ Found asset: {asset['originalFileName']} (ID: {asset['id']})")
        return asset
    print("❌ Asset not found.")
    return None


def delete_asset(asset_id):
    url = f"{IMMICH_API_URL}/assets"
    payload = json.dumps({
        "force": True,
        "ids": [asset_id]
    })
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY
    }

    print(f"🗑 Sending DELETE to {url} to delete asset ID: {asset_id}")
    print(f"📤 Payload: {payload}")

    response = requests.request("DELETE", url, headers=headers, data=payload)

    print(f"📥 Status: {response.status_code}")
    print(f"📦 Response body: {response.text}")
    if response.status_code == 200:
        print(f"✅ Successfully deleted asset ID: {asset_id}")


if __name__ == "__main__":
    asset = search_by_filename(TARGET_FILENAME)
    if asset:
        delete_asset(asset["id"])

