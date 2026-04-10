#!/usr/bin/env python3
"""
Generate Data Skaters player cards from local CSV + local photo files.

Assumptions:
- Traits are in traits.csv.
- Photos are in photos/ and named NICKNAME.JPG (case-insensitive extension lookup).

Example:
python generate_individual_player_card_from_traits.py --nickname DH21
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Sequence, Tuple

from PIL import Image, ImageDraw, ImageFont


CARD_WIDTH_IN = 2.5
CARD_HEIGHT_IN = 3.5
CARD_DPI = 300
CARD_WIDTH = int(CARD_WIDTH_IN * CARD_DPI)
CARD_HEIGHT = int(CARD_HEIGHT_IN * CARD_DPI)
Color = Tuple[int, int, int, int]


@dataclass
class PlayerTraits:
    nickname: str
    archetype: str
    height_cm: str
    wingspan_cm: str
    skate_size: str
    handedness: str
    birth_month: str
    reaction_time_ms: str
    resting_heart_rate: str


class FontSet:
    def __init__(self, custom_dir: Optional[Path] = None) -> None:
        self.custom_dir = custom_dir
        self._cache: Dict[Tuple[str, int], ImageFont.FreeTypeFont | ImageFont.ImageFont] = {}

    def get(self, style: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        key = (style, size)
        if key in self._cache:
            return self._cache[key]

        font = self._load_style(style, size)
        self._cache[key] = font
        return font

    def _load_style(self, style: str, size: int):
        candidates = []

        if self.custom_dir:
            barlow_map = {
                "regular": ["Barlow-Regular.ttf", "BarlowCondensed-Regular.ttf"],
                "bold": ["Barlow-Bold.ttf", "BarlowCondensed-Bold.ttf"],
                "heavy": ["Barlow-Black.ttf", "BarlowCondensed-Black.ttf"],
                "italic": ["Barlow-Italic.ttf", "BarlowCondensed-Italic.ttf"],
            }
            for filename in barlow_map.get(style, []):
                candidates.append(self.custom_dir / filename)

        windows_fonts = Path("C:/Windows/Fonts")
        windows_map = {
            "regular": ["arial.ttf", "segoeui.ttf"],
            "bold": ["arialbd.ttf", "seguisb.ttf", "segoeuib.ttf"],
            "heavy": ["arialbd.ttf", "seguisb.ttf", "segoeuib.ttf"],
            "italic": ["ariali.ttf", "segoeuii.ttf"],
        }
        for filename in windows_map.get(style, []):
            candidates.append(windows_fonts / filename)

        for path in candidates:
            if path.exists():
                return ImageFont.truetype(str(path), size=size)

        return ImageFont.load_default()


def normalize_key(value: str) -> str:
    return "".join(ch.lower() for ch in value.strip() if ch.isalnum())


def pick_value(row: Dict[str, str], *aliases: str) -> str:
    normalized = {normalize_key(k): (v or "").strip() for k, v in row.items()}
    for alias in aliases:
        value = normalized.get(normalize_key(alias))
        if value:
            return value
    return ""


def load_traits_by_nickname(traits_csv_path: Path) -> Dict[str, PlayerTraits]:
    if not traits_csv_path.exists():
        raise FileNotFoundError(f"traits.csv not found: {traits_csv_path}")

    players: Dict[str, PlayerTraits] = {}
    with traits_csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            nickname = pick_value(row, "nickname", "Nickname")
            if not nickname:
                continue

            players[nickname.upper()] = PlayerTraits(
                nickname=nickname,
                archetype=pick_value(row, "archetype", "Archetype") or "Unknown",
                height_cm=pick_value(row, "height_cm", "Height (cm)") or "N/A",
                wingspan_cm=pick_value(row, "wingspan_cm", "Wingspan (cm)") or "N/A",
                skate_size=pick_value(row, "skate_size", "Skate Size") or "N/A",
                handedness=pick_value(row, "handedness", "Handedness") or "N/A",
                birth_month=pick_value(row, "birth_month", "Birth Month", "Birth MOnth") or "N/A",
                reaction_time_ms=pick_value(row, "reaction_time_ms", "Reaction Time (ms)") or "N/A",
                resting_heart_rate=pick_value(row, "resting_heart_rate", "Resting Heart Rate") or "N/A",
            )

    return players


def load_logo_images(logos_dir: Path) -> Dict[str, Optional[Image.Image]]:
    mapping = {
        "dell": "dell-logo.png",
        "ps43": "ps43-foundation-logo.png",
        "lotus8": "lotus-8-esports-logo.png",
        "mfnerc": "mfnerc-logo.png",
    }
    result: Dict[str, Optional[Image.Image]] = {}
    for key, filename in mapping.items():
        path = logos_dir / filename
        if path.exists():
            result[key] = Image.open(path).convert("RGBA")
        else:
            result[key] = None
    return result


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def lerp_color(c1: Sequence[int], c2: Sequence[int], t: float) -> Color:
    return (
        int(lerp(c1[0], c2[0], t)),
        int(lerp(c1[1], c2[1], t)),
        int(lerp(c1[2], c2[2], t)),
        int(lerp(c1[3], c2[3], t)),
    )


def gradient_vertical(size: Tuple[int, int], stops: Sequence[Tuple[float, Color]]) -> Image.Image:
    width, height = size
    img = Image.new("RGBA", size)
    draw = ImageDraw.Draw(img)

    sorted_stops = sorted(stops, key=lambda x: x[0])
    for y in range(height):
        p = y / max(1, height - 1)
        left = sorted_stops[0]
        right = sorted_stops[-1]
        for i in range(len(sorted_stops) - 1):
            if sorted_stops[i][0] <= p <= sorted_stops[i + 1][0]:
                left = sorted_stops[i]
                right = sorted_stops[i + 1]
                break

        span = max(1e-9, right[0] - left[0])
        t = max(0.0, min(1.0, (p - left[0]) / span))
        color = lerp_color(left[1], right[1], t)
        draw.line([(0, y), (width, y)], fill=color)

    return img


def draw_centered_text(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, font, fill: Tuple[int, int, int, int]) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x - tw // 2, y - th // 2), text, font=font, fill=fill)


def draw_right_text(draw: ImageDraw.ImageDraw, text: str, right_x: int, y: int, font, fill: Tuple[int, int, int, int]) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((right_x - tw, y), text, font=font, fill=fill)


def draw_logo_slot(base: Image.Image, logo: Optional[Image.Image], label: str, x: int, y: int, w: int, h: int, fonts: FontSet) -> None:
    draw = ImageDraw.Draw(base)
    if logo is None:
        draw.rounded_rectangle((x, y, x + w, y + h), radius=6, fill=(255, 255, 255, 28))
        font = fonts.get("bold", int(h * 0.35))
        draw_centered_text(draw, label, x + w // 2, y + h // 2, font, (255, 255, 255, 255))
        return

    slot = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    iw, ih = logo.size
    scale = min(w / iw, h / ih)
    nw = max(1, int(iw * scale))
    nh = max(1, int(ih * scale))
    resized = logo.resize((nw, nh), Image.Resampling.LANCZOS)
    ox = (w - nw) // 2
    oy = (h - nh) // 2
    slot.alpha_composite(resized, (ox, oy))
    base.alpha_composite(slot, (x, y))


def cover_resize(image: Image.Image, target_w: int, target_h: int) -> Image.Image:
    iw, ih = image.size
    scale = max(target_w / iw, target_h / ih)
    nw = max(1, int(iw * scale))
    nh = max(1, int(ih * scale))
    resized = image.resize((nw, nh), Image.Resampling.LANCZOS)

    left = (nw - target_w) // 2
    top = (nh - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def find_player_photo(photos_dir: Path, nickname: str) -> Optional[Image.Image]:
    # Prefer the exact requested convention NICKNAME.JPG, then fall back to common variants.
    candidates = [
        photos_dir / f"{nickname.upper()}.JPG",
        photos_dir / f"{nickname.upper()}.jpg",
        photos_dir / f"{nickname}.JPG",
        photos_dir / f"{nickname}.jpg",
    ]
    for path in candidates:
        if path.exists():
            return Image.open(path).convert("RGBA")

    for path in photos_dir.glob("*.*"):
        if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"} and path.stem.upper() == nickname.upper():
            return Image.open(path).convert("RGBA")

    return None


def draw_front(player: PlayerTraits, photo: Optional[Image.Image], fonts: FontSet) -> Image.Image:
    card = gradient_vertical(
        (CARD_WIDTH, CARD_HEIGHT),
        [
            (0.0, (0, 27, 58, 255)),
            (0.5, (0, 59, 111, 255)),
            (1.0, (0, 16, 32, 255)),
        ],
    )
    draw = ImageDraw.Draw(card)

    photo_h = int(CARD_HEIGHT * 0.72)
    if photo is not None:
        card.alpha_composite(cover_resize(photo, CARD_WIDTH, photo_h), (0, 0))
    else:
        placeholder = gradient_vertical((CARD_WIDTH, photo_h), [(0.0, (0, 34, 68, 255)), (1.0, (0, 27, 58, 255))])
        card.alpha_composite(placeholder, (0, 0))

    photo_overlay = gradient_vertical(
        (CARD_WIDTH, photo_h),
        [
            (0.35, (0, 27, 58, 0)),
            (0.7, (0, 27, 58, 160)),
            (1.0, (0, 27, 58, 250)),
        ],
    )
    card.alpha_composite(photo_overlay, (0, 0))

    draw.text((36, 36), "DATA SKATERS", font=fonts.get("bold", 22), fill=(255, 255, 255, 217))
    draw.rectangle((36, 64, 216, 67), fill=(0, 118, 206, 255))

    plate_y = photo_h - 20
    draw.rectangle((0, plate_y, CARD_WIDTH, CARD_HEIGHT), fill=(0, 20, 40, 255))
    draw.rectangle((0, plate_y, CARD_WIDTH, plate_y + 5), fill=(0, 118, 206, 255))

    draw.text((34, plate_y + 36), player.nickname.upper(), font=fonts.get("heavy", 86), fill=(255, 255, 255, 255))
    draw.text((36, plate_y + 148), "ARCHETYPE", font=fonts.get("bold", 22), fill=(91, 179, 232, 255))
    draw.text((36, plate_y + 174), player.archetype.upper(), font=fonts.get("heavy", 52), fill=(255, 255, 255, 255))

    draw.rectangle((2, 2, CARD_WIDTH - 3, CARD_HEIGHT - 3), outline=(0, 118, 206, 128), width=4)
    draw.rectangle((8, 8, CARD_WIDTH - 9, CARD_HEIGHT - 9), outline=(255, 255, 255, 10), width=2)

    return card


def draw_back(player: PlayerTraits, logos: Dict[str, Optional[Image.Image]], fonts: FontSet) -> Image.Image:
    card = Image.new("RGBA", (CARD_WIDTH, CARD_HEIGHT), (250, 252, 255, 255))
    draw = ImageDraw.Draw(card)

    draw.rectangle((2, 2, CARD_WIDTH - 3, CARD_HEIGHT - 3), outline=(30, 112, 174, 170), width=4)
    draw.rectangle((8, 8, CARD_WIDTH - 9, CARD_HEIGHT - 9), outline=(22, 57, 84, 28), width=2)

    draw.rectangle((0, 0, CARD_WIDTH, 90), fill=(0, 118, 206, 255))
    draw.text((36, 20), "DATA SKATERS", font=fonts.get("heavy", 52), fill=(255, 255, 255, 255))

    draw.text((36, 112), player.nickname.upper(), font=fonts.get("heavy", 64), fill=(20, 36, 52, 255))
    draw.text((56, 186), "PLAYER TRAITS", font=fonts.get("bold", 24), fill=(33, 92, 145, 255))

    stats_rows = [
        ("HEIGHT (CM)", player.height_cm, "WINGSPAN (CM)", player.wingspan_cm),
        ("SKATE SIZE", player.skate_size, "HANDEDNESS", player.handedness),
        ("BIRTH MONTH", player.birth_month, "REACTION (MS)", player.reaction_time_ms),
        ("RESTING HR", player.resting_heart_rate, "ARCHETYPE", player.archetype),
    ]

    table_x = 20
    table_y = 250
    table_w = CARD_WIDTH - 40
    row_h = 84
    col_w = table_w // 2
    table_h = row_h * len(stats_rows)

    draw.rounded_rectangle((table_x, table_y, table_x + table_w, table_y + table_h), radius=8, fill=(255, 255, 255, 255))

    for ri, row in enumerate(stats_rows):
        y = table_y + ri * row_h
        draw.rectangle((table_x, y, table_x + table_w, y + row_h), fill=(255, 255, 255, 255))
        if ri < len(stats_rows) - 1:
            draw.line((table_x + 10, y + row_h, table_x + table_w - 10, y + row_h), fill=(196, 38, 38, 210), width=2)

        draw.text((table_x + 32, y + 6), row[0], font=fonts.get("bold", 19), fill=(33, 92, 145, 255))
        draw.text((table_x + 32, y + 32), str(row[1]), font=fonts.get("heavy", 44), fill=(20, 36, 52, 255))

        right_col_x = table_x + col_w + 12
        draw.text((right_col_x, y + 6), row[2], font=fonts.get("bold", 19), fill=(33, 92, 145, 255))
        right_value = str(row[3])
        if row[2] == "ARCHETYPE" and right_value.strip().lower() == "defensive defenceman":
            draw.multiline_text(
                (right_col_x, y + 26),
                "DEFENSIVE\nDEFENCEMAN",
                font=fonts.get("heavy", 26),
                fill=(20, 36, 52, 255),
                spacing=0,
            )
        else:
            draw.text((right_col_x, y + 32), right_value, font=fonts.get("heavy", 44), fill=(20, 36, 52, 255))

    draw.line((table_x + col_w, table_y + 10, table_x + col_w, table_y + table_h - 10), fill=(196, 38, 38, 210), width=2)

    logo_labels = ["PS43", "LOTUS 8", "MFNERC", "DELL"]
    logo_images = [logos.get("ps43"), logos.get("lotus8"), logos.get("mfnerc"), logos.get("dell")]
    slot_w = 150
    slot_h = 64
    gap = 18
    total_w = slot_w * len(logo_images) + gap * (len(logo_images) - 1)
    logos_x = (CARD_WIDTH - total_w) // 2
    logos_y = CARD_HEIGHT - 108

    draw.rectangle((0, logos_y - 54, CARD_WIDTH, CARD_HEIGHT), fill=(0, 20, 40, 245))
    draw.rectangle((logos_x, logos_y - 16, logos_x + total_w, logos_y - 13), fill=(0, 118, 206, 255))
    draw_centered_text(draw, "POWERED BY", CARD_WIDTH // 2, logos_y - 30, fonts.get("bold", 16), (255, 255, 255, 77))

    for i, logo in enumerate(logo_images):
        x = logos_x + i * (slot_w + gap)
        draw_logo_slot(card, logo, logo_labels[i], x, logos_y, slot_w, slot_h, fonts)

    draw_centered_text(draw, "datadunkers.ca  .  #dataskaters", CARD_WIDTH // 2, CARD_HEIGHT - 22, fonts.get("bold", 18), (255, 255, 255, 51))

    return card


def combine_front_back(front: Image.Image, back: Image.Image) -> Image.Image:
    combo = Image.new("RGBA", (CARD_WIDTH * 2, CARD_HEIGHT), (6, 15, 30, 255))
    combo.alpha_composite(back, (0, 0))
    combo.alpha_composite(front, (CARD_WIDTH, 0))
    return combo


def generate_player_card_from_traits(
    nickname: str,
    traits_csv: Path,
    photos_dir: Path,
    logos_dir: Path,
    output_path: Optional[Path] = None,
    fonts_dir: Optional[Path] = None,
) -> Dict[str, Path]:

    players = load_traits_by_nickname(traits_csv)
    player = players.get(nickname.upper())
    if player is None:
        raise ValueError(f"Nickname '{nickname}' not found in {traits_csv}")

    photo = find_player_photo(photos_dir, nickname)

    fonts = FontSet(custom_dir=fonts_dir)
    logos = load_logo_images(logos_dir)

    front = draw_front(player, photo, fonts)
    back = draw_back(player, logos, fonts)

    combined = combine_front_back(front, back)

    if output_path is None:
        output_path = Path(f"{nickname.lower()}-traits-card.png")
    elif not output_path.suffix:
        output_path = output_path.with_suffix(".png")

    front_path = output_path.with_name(f"{output_path.stem}-front{output_path.suffix}")
    back_path = output_path.with_name(f"{output_path.stem}-back{output_path.suffix}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    combined.convert("RGB").save(output_path, format="PNG", dpi=(CARD_DPI, CARD_DPI))
    front.convert("RGB").save(front_path, format="PNG", dpi=(CARD_DPI, CARD_DPI))
    back.convert("RGB").save(back_path, format="PNG", dpi=(CARD_DPI, CARD_DPI))
    return {
        "combined": output_path,
        "front": front_path,
        "back": back_path,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Data Skaters player card from local traits.csv and photos/")
    parser.add_argument("--nickname", required=True, help="Nickname key in traits.csv and photo filename stem")
    parser.add_argument("--traits-csv", default="traits.csv")
    parser.add_argument("--photos-dir", default="photos")
    parser.add_argument("--logos-dir", default="docs/card-creator")
    parser.add_argument("--fonts-dir", default=None)
    parser.add_argument("--output", default=None)
    return parser


def main() -> None:
    args = _build_parser().parse_args()

    outputs = generate_player_card_from_traits(
        nickname=args.nickname,
        traits_csv=Path(args.traits_csv),
        photos_dir=Path(args.photos_dir),
        logos_dir=Path(args.logos_dir),
        output_path=Path(args.output) if args.output else None,
        fonts_dir=Path(args.fonts_dir) if args.fonts_dir else None,
    )
    print(f"Cards generated: {outputs['combined']}, {outputs['front']}, {outputs['back']}")


if __name__ == "__main__":
    main()
