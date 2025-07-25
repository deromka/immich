import requests
import json

IMMICH_API_URL = "http://192.168.2.54:2283/api"
API_KEY = "LMaVxA03VIxImcV2mhMSGVFEmQxpA4cagRmPjw0V35Q"

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "x-api-key": API_KEY,
}

def debug_metadata_page(page=1):
    body = {
        "fileExtension": "webp",
        "page": page,
        "size": 10
    }
    response = requests.post(f"{IMMICH_API_URL}/search/metadata", headers=HEADERS, json=body)
    print(f"📄 Status: {response.status_code}")
    print("🧾 Response JSON structure:\n")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    debug_metadata_page()

