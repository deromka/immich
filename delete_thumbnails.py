import requests
import json
import subprocess
import time
import psutil
from datetime import datetime, timezone

# 🗓️ Cutoff: Only delete assets created after this timestamp
CUTOFF_DATE = datetime(2025, 7, 17, tzinfo=timezone.utc)
CUTOFF_ISO = CUTOFF_DATE.isoformat()

# 🔧 Immich API Config
API_URL = "http://192.168.2.54:2283/api"
API_KEY = "LMaVxA03VIxImcV2mhMSGVFEmQxpA4cagRmPjw0V35Q"
HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}
PAGE_SIZE = 1000

# 🎯 Target suffixes
TARGET_SUFFIXES = ("-thumbnail.webp", "-preview.jpeg")

def search_assets(page):
    url = f"{API_URL}/search/metadata"
    payload = {
        "page": page,
        "size": PAGE_SIZE,
        "createdAfter": CUTOFF_ISO
    }
    print(f"\n🔍 Searching page {page} after {CUTOFF_ISO}...")
    res = requests.post(url, headers=HEADERS, data=json.dumps(payload))

    if res.status_code != 200:
        print(f"❌ Failed search: {res.status_code} | {res.text}")
        return []

    data = res.json()
    return data.get("assets", {}).get("items", [])

def delete_assets_batch(asset_ids):
    if not asset_ids:
        return

    url = f"{API_URL}/assets"
    payload = json.dumps({
        "force": True,
        "ids": asset_ids
    })

    print(f"🗑 Deleting {len(asset_ids)} assets in batch")
    res = requests.delete(url, headers=HEADERS, data=payload)

    print(f"📦 Status: {res.status_code}")
    print(f"📬 Response body: {res.text}")
    if res.status_code in (200, 204):
        print("✅ Batch delete successful.")
    else:
        print("❌ Batch delete failed.")


def get_available_memory_mb():
    mem = psutil.virtual_memory()
    return mem.available / (1024 * 1024)  # in MB

def get_free_memory_mb():
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if line.startswith('MemFree:'):
                return int(line.split()[1]) / 1024  # kB to MB

def wait_for_memory(min_free_mb=512):
    while True:
        avail_mb = get_available_memory_mb()
        free_mem = get_free_memory_mb()
        print(f"Free memory: {free_mem:.2f} MB")
        print(f"Available memory: {avail_mb:.2f} MB")
        if avail_mb >= min_free_mb:
            print("✅ Enough available memory. Proceeding...")
            break
        else:
            print("⏳ Not enough available memory (<512MB). Waiting 120s...")
            time.sleep(120)


TASK_THRESHOLD = 20000

def wait_for_queue():
    while True:
        try:
            result = subprocess.check_output(
                ["redis-cli", "LLEN", "immich_bull:backgroundTask:wait"],
                text=True
            )
            task_count = int(result.strip())
            print(f"🧠 Redis queue length: {task_count}")
            if task_count < TASK_THRESHOLD:
                break
            else:
                print(f"⏳ Queue too full (>{TASK_THRESHOLD}). Waiting 120 seconds...")
                time.sleep(120)
        except Exception as e:
            print(f"⚠️ Redis check failed: {e}")
            break  # Optionally continue instead of hard failing



def main():
    page = 1
    total_deleted = 0

    while True:
        wait_for_memory()
        wait_for_queue()
        assets = search_assets(page)
        if not assets:
            break

        batch_ids = []
        for asset in assets:
            filename = asset.get("originalFileName", "")
            if filename.endswith(TARGET_SUFFIXES):
                print(f"📄 Matched: {filename}")
                batch_ids.append(asset["id"])

        if batch_ids:
            delete_assets_batch(batch_ids)
            total_deleted += len(batch_ids)

        print("⏳ Waiting 10 seconds before next page...")
        time.sleep(10)
        page += 1

    print(f"\n🎉 Finished. Total deleted assets: {total_deleted}")

if __name__ == "__main__":
    main()

