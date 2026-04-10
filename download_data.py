#!/usr/bin/env python3
"""Download skater traits, names, and photos from api.datadunkers.ca."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import requests


BASE_URL = "https://api.datadunkers.ca"
TRAITS_COLLECTION = "data_skaters_traits"
PHOTOS_COLLECTION = "data_skaters_photos"


def fetch_all_records(collection: str, per_page: int = 200) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    page = 1

    while True:
        response = requests.get(
            f"{BASE_URL}/api/collections/{collection}/records",
            params={"page": page, "perPage": per_page},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        items = data.get("items", [])
        if not items:
            break

        records.extend(items)

        total_pages = data.get("totalPages", page)
        if page >= total_pages:
            break
        page += 1

    return records


def write_traits_csv(records: list[dict[str, Any]], output_path: Path) -> None:
    fieldnames = [
        "nickname",
        "height_cm",
        "wingspan_cm",
        "skate_size",
        "handedness",
        "birth_month",
        "reaction_time_ms",
        "resting_heart_rate",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "nickname": record.get("nickname", ""),
                    "height_cm": record.get("height_cm", ""),
                    "wingspan_cm": record.get("wingspan_cm", ""),
                    "skate_size": record.get("skate_size", ""),
                    "handedness": record.get("handedness", ""),
                    "birth_month": record.get("birth_month", ""),
                    "reaction_time_ms": record.get("reaction_time_ms", ""),
                    "resting_heart_rate": record.get("resting_heart_rate", ""),
                }
            )


def extract_photo_filename(photo_field: Any) -> str:
    if isinstance(photo_field, list):
        return str(photo_field[0]) if photo_field else ""
    if isinstance(photo_field, str):
        return photo_field
    return ""


def sanitize_filename(value: str) -> str:
    keep = "-_.() "
    cleaned = "".join(ch for ch in value if ch.isalnum() or ch in keep).strip()
    return cleaned or "unknown"


def write_names_and_download_photos(records: list[dict[str, Any]], names_csv: Path, output_dir: Path) -> int:
    downloaded = 0

    with names_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nickname", "real_name"])
        writer.writeheader()

        for record in records:
            nickname = str(record.get("nickname", "")).strip()
            real_name = str(record.get("real_name", "") or "").strip()
            writer.writerow({"nickname": nickname, "real_name": real_name})

            photo_filename = extract_photo_filename(record.get("photo"))
            record_id = record.get("id")
            if not (nickname and photo_filename and record_id):
                continue

            photo_url = f"{BASE_URL}/api/files/{PHOTOS_COLLECTION}/{record_id}/{photo_filename}"
            photo_response = requests.get(photo_url, timeout=30)
            photo_response.raise_for_status()

            output_file = output_dir / f"{sanitize_filename(nickname)}.png"
            output_file.write_bytes(photo_response.content)
            downloaded += 1

    return downloaded


def main() -> None:
    traits = fetch_all_records(TRAITS_COLLECTION)
    photos = fetch_all_records(PHOTOS_COLLECTION)

    write_traits_csv(traits, Path("traits.csv"))
    downloaded_count = write_names_and_download_photos(photos, Path("names.csv"), Path("."))

    print(f"Saved traits.csv ({len(traits)} rows)")
    print(f"Saved names.csv ({len(photos)} rows)")
    print(f"Downloaded {downloaded_count} photos")


if __name__ == "__main__":
    main()