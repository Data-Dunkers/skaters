import urllib.request
import json
import ssl

PB_BASE_URL = "https://api.datadunkers.ca/api/collections"
COLLECTIONS = ["data_skaters_photos", "data_skaters_traits", "data_skaters_shots"]
# By default, use an unverified context if there are SSL issues, though https should be fine.
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_records(collection):
    url = f"{PB_BASE_URL}/{collection}/records?perPage=500"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            return data.get('items', [])
    except Exception as e:
        print(f"Error fetching from {collection}: {e}")
        return []

def update_record(collection, record_id):
    url = f"{PB_BASE_URL}/{collection}/records/{record_id}"
    payload = json.dumps({"event_key": "demo"}).encode('utf-8')
    try:
        req = urllib.request.Request(url, data=payload, method='PATCH')
        req.add_header('Content-Type', 'application/json')
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, context=ctx) as response:
            return response.status == 200
    except Exception as e:
        print(f"Error updating {collection} id {record_id}: {e}")
        return False

def main():
    for collection in COLLECTIONS:
        print(f"Processing {collection}...")
        records = fetch_records(collection)
        print(f"Found {len(records)} records in {collection}")
        
        updated_count = 0
        for rec in records:
            # We update if event_key is missing or empty
            if rec.get('event_key') != 'demo':
                if update_record(collection, rec['id']):
                    updated_count += 1
        
        print(f"Successfully updated {updated_count} records in {collection}.")

if __name__ == "__main__":
    main()
