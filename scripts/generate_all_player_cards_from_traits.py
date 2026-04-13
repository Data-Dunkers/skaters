#!/usr/bin/env python3
"""Generate cards for every nickname in traits.csv by invoking the single-player generator.

Example:
python generate_all_player_cards_from_traits.py
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path
from typing import Iterable


def normalize_key(value: str) -> str:
    return "".join(ch.lower() for ch in value.strip() if ch.isalnum())


def read_nicknames(traits_csv: Path) -> list[str]:
    if not traits_csv.exists():
        raise FileNotFoundError(f"traits.csv not found: {traits_csv}")

    nicknames: list[str] = []
    seen: set[str] = set()

    with traits_csv.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            return []

        nickname_column = None
        for field in reader.fieldnames:
            if normalize_key(field) == "nickname":
                nickname_column = field
                break

        if nickname_column is None:
            raise ValueError("traits.csv is missing a nickname column")

        for row in reader:
            nickname = (row.get(nickname_column) or "").strip()
            if not nickname:
                continue
            key = nickname.upper()
            if key in seen:
                continue
            seen.add(key)
            nicknames.append(nickname)

    return nicknames


def run_generator_for_nickname(
    python_executable: str,
    generator_script: Path,
    nickname: str,
    traits_csv: Path,
    photos_dir: Path,
    logos_dir: Path,
    output_dir: Path,
    fonts_dir: Path | None,
) -> subprocess.CompletedProcess[str]:
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd: list[str] = [
        python_executable,
        str(generator_script),
        "--nickname",
        nickname,
        "--traits-csv",
        str(traits_csv),
        "--photos-dir",
        str(photos_dir),
        "--logos-dir",
        str(logos_dir),
        "--output",
        str(output_dir / f"{nickname.lower()}-traits-card.png"),
    ]

    if fonts_dir is not None:
        cmd.extend(["--fonts-dir", str(fonts_dir)])

    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate cards for all players listed in traits.csv"
    )
    parser.add_argument("--traits-csv", default="traits.csv")
    parser.add_argument(
        "--generator-script", default="generate_individual_player_card_from_traits.py"
    )
    parser.add_argument("--photos-dir", default="photos")
    parser.add_argument("--logos-dir", default="docs/card-creator")
    parser.add_argument("--output-dir", default=".")
    parser.add_argument("--fonts-dir", default=None)
    parser.add_argument(
        "--stop-on-error",
        action="store_true",
        help="Stop immediately when one nickname fails",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    traits_csv = Path(args.traits_csv)
    generator_script = Path(args.generator_script)
    photos_dir = Path(args.photos_dir)
    logos_dir = Path(args.logos_dir)
    output_dir = Path(args.output_dir)
    fonts_dir = Path(args.fonts_dir) if args.fonts_dir else None

    if not generator_script.exists():
        raise FileNotFoundError(f"Generator script not found: {generator_script}")

    nicknames = read_nicknames(traits_csv)
    if not nicknames:
        print("No nicknames found in traits.csv")
        return

    print(f"Found {len(nicknames)} nickname(s). Starting generation...")

    successes = 0
    failures: list[tuple[str, str]] = []

    for index, nickname in enumerate(nicknames, start=1):
        print(f"[{index}/{len(nicknames)}] Generating cards for {nickname}...")
        result = run_generator_for_nickname(
            python_executable=sys.executable,
            generator_script=generator_script,
            nickname=nickname,
            traits_csv=traits_csv,
            photos_dir=photos_dir,
            logos_dir=logos_dir,
            output_dir=output_dir,
            fonts_dir=fonts_dir,
        )

        if result.returncode == 0:
            successes += 1
            if result.stdout.strip():
                print(result.stdout.strip())
            continue

        error_text = result.stderr.strip() or result.stdout.strip() or "Unknown error"
        failures.append((nickname, error_text))
        print(f"Failed for {nickname}: {error_text}")

        if args.stop_on_error:
            break

    print()
    print(f"Completed. Success: {successes}. Failed: {len(failures)}.")
    if failures:
        print("Failures:")
        for nickname, error in failures:
            print(f"- {nickname}: {error}")


if __name__ == "__main__":
    main()
