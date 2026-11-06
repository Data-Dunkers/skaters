"""Upload a folder of photos named like PS43-David_Hay.jpg to the PocketBase photos collection.

Nickname = part before the first '-', real_name = the rest with '_' replaced by spaces.

Edit the settings below, then run: python upload_photo_folder.py
"""
import mimetypes
from pathlib import Path

import requests

# Settings
FOLDER = r"C:\Users\username\Downloads\upload"
EVENT_KEY = "OS"
GROUP = "0"
SKIP_EXISTING = True  # skip if a record with the same nickname and event_key exists
DRY_RUN = False  # print what would be uploaded without sending anything
POCKETBASE_URL = "https://api.datadunkers.ca"
COLLECTION = "data_skaters_photos"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def parse_name(path: Path):
    nickname, sep, rest = path.stem.partition("-")
    if not rest:
        rest = ''
    return nickname.strip(), rest.replace("-", " ").title().strip()


def exists(url, nickname, event_key):
    flt = f'nickname="{nickname}" && event_key="{event_key}"'
    r = requests.get(url, params={"filter": flt, "perPage": 1})
    r.raise_for_status()
    return r.json().get("totalItems", 0) > 0


url = f"{POCKETBASE_URL}/api/collections/{COLLECTION}/records"
files = sorted(f for f in Path(FOLDER).iterdir() if f.suffix.lower() in EXTENSIONS)
ok = failed = skipped = 0

for f in files:
    parsed = parse_name(f)
    if not parsed:
        print(f"SKIP (bad filename): {f.name}")
        skipped += 1
        continue
    nickname, real_name = parsed
    if DRY_RUN:
        print(f"DRY RUN: {f.name} -> nickname={nickname!r}, real_name={real_name!r}")
        continue
    try:
        if SKIP_EXISTING and exists(url, nickname, EVENT_KEY):
            print(f"SKIP (exists): {nickname}")
            skipped += 1
            continue
        data = {"nickname": nickname, "real_name": real_name, "event_key": EVENT_KEY}
        if GROUP:
            data["group"] = GROUP
        mime = mimetypes.guess_type(f.name)[0] or "application/octet-stream"
        with open(f, "rb") as fh:
            r = requests.post(url, data=data, files={"photo": (f.name, fh, mime)})
        if r.ok:
            print(f"OK: {nickname} ({real_name})")
            ok += 1
        else:
            print(f"FAILED: {f.name}: {r.status_code} {r.text}")
            failed += 1
    except Exception as e:
        print(f"FAILED: {f.name}: {e}")
        failed += 1
print(f"Done. uploaded={ok} failed={failed} skipped={skipped}")
