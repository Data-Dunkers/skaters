#!/usr/bin/env python3
"""
Generate Data Skaters player cards locally from PocketBase + input parameters.

Dependencies:
- pillow (pip install pillow)
- requests

Example:
python generate_individual_player_card.py --nickname PS43 --number 43 --position Centre --height 203 --hand Right --month April --goals 12 --hot-zone TL --accuracy 74 --archetype Sniper --side both --output ps43-card.png
"""

from __future__ import annotations

import argparse
from io import BytesIO
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Sequence, Tuple

import requests
from PIL import Image, ImageDraw, ImageFont


POCKETBASE_URL = "https://api.datadunkers.ca"
COLLECTION_NAME = "data_skaters_photos"
CARD_WIDTH = 750
CARD_HEIGHT = 1050
HOT_ZONE_MAP = {
    "TL": "Top Left",
    "TR": "Top Right",
    "BL": "Bottom Left",
    "BR": "Bottom Right",
    "FH": "Five Hole",
}


Color = Tuple[int, int, int, int]


@dataclass
class PlayerCardData:
    nickname: str
    number: str
    position: str
    height: str
    hand: str
    month: str
    goals: str
    hot_zone: str
    accuracy: str
    archetype: str
    side: str = "both"
    name: Optional[str] = None


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
            # Optional Barlow files if user places them here.
            barlow_map = {
                "regular": ["Barlow-Regular.ttf", "BarlowCondensed-Regular.ttf"],
                "bold": ["Barlow-Bold.ttf", "BarlowCondensed-Bold.ttf"],
                "heavy": ["Barlow-Black.ttf", "BarlowCondensed-Black.ttf"],
                "italic": ["Barlow-Italic.ttf", "BarlowCondensed-Italic.ttf"],
            }
            for filename in barlow_map.get(style, []):
                candidates.append(self.custom_dir / filename)

        # Windows fallbacks.
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


def split_name(name: str) -> Tuple[str, str]:
    parts = (name or "Player Name").strip().split()
    if not parts:
        return "PLAYER", "NAME"
    if len(parts) == 1:
        return parts[0], ""
    return " ".join(parts[:-1]), parts[-1]


def normalize_hot_zone(value: str) -> str:
    zone = (value or "").strip()
    if not zone:
        return "Top Left"

    mapped = HOT_ZONE_MAP.get(zone.upper())
    if mapped:
        return mapped

    return zone


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


def fetch_pocketbase_record(nickname: str, pocketbase_url: str = POCKETBASE_URL, collection_name: str = COLLECTION_NAME, timeout: int = 20) -> Dict[str, str]:
    if not nickname.strip():
        return {"real_name": "", "photo_url": ""}

    escaped = nickname.replace('"', '\\"')
    params = {
        "perPage": 1,
        "page": 1,
        "filter": f'nickname="{escaped}"',
        "sort": "-created",
    }
    url = f"{pocketbase_url}/api/collections/{collection_name}/records"
    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    payload = response.json()

    items = payload.get("items") or []
    if not items:
        return {"real_name": "", "photo_url": ""}

    record = items[0]
    photo = record.get("photo")
    photo_filename = photo[0] if isinstance(photo, list) and photo else photo

    photo_url = ""
    if photo_filename:
        photo_url = f"{pocketbase_url}/api/files/{collection_name}/{record['id']}/{photo_filename}"

    return {
        "real_name": (record.get("real_name") or "").strip(),
        "photo_url": photo_url,
    }


def fetch_photo(photo_url: str, timeout: int = 30) -> Optional[Image.Image]:
    if not photo_url:
        return None

    response = requests.get(photo_url, timeout=timeout)
    response.raise_for_status()
    return Image.open(BytesIO(response.content)).convert("RGBA")


def cover_resize(image: Image.Image, target_w: int, target_h: int) -> Image.Image:
    iw, ih = image.size
    scale = max(target_w / iw, target_h / ih)
    nw = max(1, int(iw * scale))
    nh = max(1, int(ih * scale))
    resized = image.resize((nw, nh), Image.Resampling.LANCZOS)

    left = (nw - target_w) // 2
    top = (nh - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def draw_front(data: PlayerCardData, name: str, player_photo: Optional[Image.Image], fonts: FontSet) -> Image.Image:
    card = gradient_vertical(
        (CARD_WIDTH, CARD_HEIGHT),
        [
            (0.0, (0, 27, 58, 255)),
            (0.5, (0, 59, 111, 255)),
            (1.0, (0, 16, 32, 255)),
        ],
    )
    draw = ImageDraw.Draw(card)

    photo_h = int(CARD_HEIGHT * 0.68)
    if player_photo is not None:
        fitted = cover_resize(player_photo, CARD_WIDTH, photo_h)
        card.alpha_composite(fitted, (0, 0))
    else:
        placeholder = gradient_vertical((CARD_WIDTH, photo_h), [(0.0, (0, 34, 68, 255)), (1.0, (0, 27, 58, 255))])
        card.alpha_composite(placeholder, (0, 0))
        pdraw = ImageDraw.Draw(card)
        pdraw.ellipse((CARD_WIDTH // 2 - 110, int(photo_h * 0.42) - 110, CARD_WIDTH // 2 + 110, int(photo_h * 0.42) + 110), fill=(255, 255, 255, 16))
        pdraw.ellipse((CARD_WIDTH // 2 - 160, int(photo_h * 0.85) - 80, CARD_WIDTH // 2 + 160, int(photo_h * 0.85) + 80), fill=(255, 255, 255, 10))

    photo_overlay = gradient_vertical(
        (CARD_WIDTH, photo_h),
        [
            (0.3, (0, 27, 58, 0)),
            (0.6, (0, 27, 58, 153)),
            (1.0, (0, 27, 58, 250)),
        ],
    )
    card.alpha_composite(photo_overlay, (0, 0))

    stripe = Image.new("RGBA", (CARD_WIDTH, CARD_HEIGHT), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(stripe)
    sdraw.polygon(
        [(0, photo_h - 120), (CARD_WIDTH, photo_h - 200), (CARD_WIDTH, photo_h - 160), (0, photo_h - 80)],
        fill=(0, 118, 206, 45),
    )
    card.alpha_composite(stripe)

    draw.text((36, 36), "DATA SKATERS", font=fonts.get("bold", 22), fill=(255, 255, 255, 217))
    draw.rectangle((36, 64, 216, 67), fill=(0, 118, 206, 255))

    ghost_font = fonts.get("heavy", 130)
    main_num_font = fonts.get("heavy", 72)
    draw_right_text(draw, f"#{data.number}", CARD_WIDTH - 30, 10, ghost_font, (255, 255, 255, 20))
    draw_right_text(draw, f"#{data.number}", CARD_WIDTH - 32, 28, main_num_font, (255, 255, 255, 230))

    plate_y = photo_h - 10
    draw.rectangle((0, plate_y, CARD_WIDTH, CARD_HEIGHT), fill=(0, 20, 40, 255))
    draw.rectangle((0, plate_y, CARD_WIDTH, plate_y + 5), fill=(0, 118, 206, 255))

    draw.text((36, plate_y + 22), data.position.upper(), font=fonts.get("bold", 24), fill=(91, 179, 232, 255))

    first_name, last_name = split_name(name)
    draw.text((34, plate_y + 52), first_name.upper(), font=fonts.get("bold", 56), fill=(255, 255, 255, 179))
    draw.text((34, plate_y + 102), last_name.upper(), font=fonts.get("heavy", 80), fill=(255, 255, 255, 255))

    draw_right_text(draw, f"{data.hand.upper()} HAND", CARD_WIDTH - 36, plate_y + 28, fonts.get("bold", 20), (255, 255, 255, 128))
    draw_right_text(draw, str(data.height), CARD_WIDTH - 36, plate_y + 56, fonts.get("bold", 24), (255, 255, 255, 153))

    stats = [("ZONE", data.hot_zone), ("GOALS", data.goals), ("TYPE", data.archetype)]
    stats_y = plate_y + 200
    sw = CARD_WIDTH // 3

    for i, (label, value) in enumerate(stats):
        x0 = i * sw
        x_mid = x0 + sw // 2
        if i > 0:
            draw.line((x0, stats_y - 16, x0, stats_y + 60), fill=(255, 255, 255, 26), width=1)

        draw_centered_text(draw, label, x_mid, stats_y + 18, fonts.get("bold", 20), (91, 179, 232, 255))
        draw_centered_text(draw, str(value), x_mid, stats_y + 48, fonts.get("heavy", 24), (255, 255, 255, 255))

    draw.rectangle((2, 2, CARD_WIDTH - 3, CARD_HEIGHT - 3), outline=(0, 118, 206, 128), width=4)
    draw.rectangle((8, 8, CARD_WIDTH - 9, CARD_HEIGHT - 9), outline=(255, 255, 255, 10), width=2)

    return card


def draw_back(data: PlayerCardData, name: str, logos: Dict[str, Optional[Image.Image]], fonts: FontSet) -> Image.Image:
    card = gradient_vertical(
        (CARD_WIDTH, CARD_HEIGHT),
        [
            (0.0, (0, 20, 40, 255)),
            (0.5, (0, 34, 68, 255)),
            (1.0, (0, 16, 32, 255)),
        ],
    )
    draw = ImageDraw.Draw(card)

    # Rink lines.
    draw.ellipse((CARD_WIDTH // 2 - 200, 280 - 200, CARD_WIDTH // 2 + 200, 280 + 200), outline=(0, 118, 206, 31), width=3)
    draw.ellipse((CARD_WIDTH // 2 - 20, 280 - 20, CARD_WIDTH // 2 + 20, 280 + 20), outline=(0, 118, 206, 31), width=3)
    draw.line((60, 140, CARD_WIDTH - 60, 140), fill=(0, 118, 206, 31), width=3)
    draw.line((60, 420, CARD_WIDTH - 60, 420), fill=(0, 118, 206, 31), width=3)
    draw.line((60, 280, CARD_WIDTH - 60, 280), fill=(220, 30, 30, 38), width=3)

    draw.rectangle((2, 2, CARD_WIDTH - 3, CARD_HEIGHT - 3), outline=(0, 118, 206, 128), width=4)
    draw.rectangle((8, 8, CARD_WIDTH - 9, CARD_HEIGHT - 9), outline=(255, 255, 255, 10), width=2)

    draw.rectangle((0, 0, CARD_WIDTH, 90), fill=(0, 118, 206, 255))
    draw.rectangle((0, 60, CARD_WIDTH, 90), fill=(0, 118, 206, 255))

    draw.text((36, 20), "DATA SKATERS", font=fonts.get("heavy", 52), fill=(255, 255, 255, 255))
    draw_right_text(draw, f"#{data.number}", CARD_WIDTH - 36, 24, fonts.get("bold", 36), (255, 255, 255, 153))

    first_name, last_name = split_name(name)
    draw.text((36, 108), first_name.upper(), font=fonts.get("bold", 28), fill=(255, 255, 255, 128))
    draw.text((36, 136), last_name.upper(), font=fonts.get("heavy", 52), fill=(255, 255, 255, 255))
    draw.text((36, 196), data.position.upper(), font=fonts.get("bold", 22), fill=(91, 179, 232, 255))

    stats_rows = [
        ("HEIGHT", f"{data.height} cm", "NUMBER", data.number),
        ("BIRTH MONTH", data.month, "SHOOTS", data.hand),
        ("GOALS", data.goals, "HOT ZONE", data.hot_zone),
        ("ACCURACY", f"{data.accuracy}%", "ARCHETYPE", data.archetype),
    ]

    table_y = 265
    row_h = 74
    col_w = CARD_WIDTH // 2

    for ri, row in enumerate(stats_rows):
        y = table_y + ri * row_h
        bg = (0, 118, 206, 26) if ri % 2 == 0 else (255, 255, 255, 10)
        draw.rectangle((0, y, CARD_WIDTH, y + row_h), fill=bg)
        draw.line((0, y + row_h, CARD_WIDTH, y + row_h), fill=(255, 255, 255, 15), width=1)
        draw.line((CARD_WIDTH // 2, y + 8, CARD_WIDTH // 2, y + row_h - 8), fill=(255, 255, 255, 15), width=1)

        draw.text((36, y + 12), row[0], font=fonts.get("bold", 18), fill=(91, 179, 232, 255))
        draw.text((36, y + 32), str(row[1]), font=fonts.get("heavy", 34), fill=(255, 255, 255, 255))

        draw.text((col_w + 30, y + 12), row[2], font=fonts.get("bold", 18), fill=(91, 179, 232, 255))
        draw.text((col_w + 30, y + 32), str(row[3]), font=fonts.get("heavy", 34), fill=(255, 255, 255, 255))

    logo_labels = ["PS43", "LOTUS 8", "MFNERC", "DELL"]
    logo_images = [logos.get("ps43"), logos.get("lotus8"), logos.get("mfnerc"), logos.get("dell")]
    slot_w = 150
    slot_h = 64
    gap = 18
    total_w = slot_w * len(logo_images) + gap * (len(logo_images) - 1)
    logos_x = (CARD_WIDTH - total_w) // 2
    logos_y = CARD_HEIGHT - 108

    draw.rectangle((logos_x, logos_y - 16, logos_x + total_w, logos_y - 13), fill=(0, 118, 206, 255))
    draw_centered_text(draw, "POWERED BY", CARD_WIDTH // 2, logos_y - 30, fonts.get("bold", 16), (255, 255, 255, 77))

    for i, logo in enumerate(logo_images):
        x = logos_x + i * (slot_w + gap)
        draw_logo_slot(card, logo, logo_labels[i], x, logos_y, slot_w, slot_h, fonts)

    draw_centered_text(draw, "datadunkers.ca  ·  #dataskaters", CARD_WIDTH // 2, CARD_HEIGHT - 22, fonts.get("bold", 18), (255, 255, 255, 51))
    return card


def combine_front_back(front: Image.Image, back: Image.Image) -> Image.Image:
    combo = Image.new("RGBA", (CARD_WIDTH * 2, CARD_HEIGHT), (6, 15, 30, 255))
    combo.alpha_composite(front, (0, 0))
    combo.alpha_composite(back, (CARD_WIDTH, 0))
    return combo


def generate_player_card(
    nickname: str,
    number: str,
    position: str,
    height: str,
    hand: str,
    month: str,
    goals: str,
    hot_zone: str,
    accuracy: str,
    archetype: str,
    side: str = "both",
    name: Optional[str] = None,
    output_path: str | Path | None = None,
    pocketbase_url: str = POCKETBASE_URL,
    collection_name: str = COLLECTION_NAME,
    logos_dir: Optional[str | Path] = None,
    fonts_dir: Optional[str | Path] = None,
    timeout: int = 20,
) -> Path:
    """Generate a local PNG that matches the card-creator API layout.

    Args:
        nickname: Player nickname used to look up record in PocketBase.
        number: Jersey number.
        position: Position label (e.g., Centre).
        height: Height in cm as string/int.
        hand: Handedness label (Right/Left/Ambidextrous).
        month: Birth month.
        goals: Goals stat.
        hot_zone: Hot zone label.
        accuracy: Accuracy percentage number (without %).
        archetype: Archetype label.
        side: one of front/back/both.
        name: Optional override for display name. If missing, uses PocketBase real_name, then nickname.
        output_path: PNG output path. Defaults to <nickname>.png when omitted.
        pocketbase_url: PocketBase base URL.
        collection_name: PocketBase collection for photo records.
        logos_dir: Directory containing card logo PNGs. Defaults to docs/card-creator.
        fonts_dir: Optional directory of Barlow font files for closer visual parity.
        timeout: HTTP timeout seconds.

    Returns:
        Path to the generated PNG file.
    """
    side_norm = side.strip().lower()
    if side_norm not in {"front", "back", "both"}:
        raise ValueError("side must be one of: front, back, both")

    record = fetch_pocketbase_record(
        nickname=nickname,
        pocketbase_url=pocketbase_url,
        collection_name=collection_name,
        timeout=timeout,
    )

    resolved_name = (name or record.get("real_name") or nickname or "Player Name").strip()

    photo_image = None
    photo_url = record.get("photo_url") or ""
    if photo_url:
        try:
            response = requests.get(photo_url, timeout=timeout)
            response.raise_for_status()
            photo_image = Image.open(BytesIO(response.content)).convert("RGBA")
        except Exception:
            photo_image = None

    data = PlayerCardData(
        nickname=nickname,
        number=str(number),
        position=str(position),
        height=str(height),
        hand=str(hand),
        month=str(month),
        goals=str(goals),
        hot_zone=normalize_hot_zone(str(hot_zone)),
        accuracy=str(accuracy),
        archetype=str(archetype),
        side=side_norm,
        name=resolved_name,
    )

    base_dir = Path(__file__).resolve().parent
    logos_path = Path(logos_dir) if logos_dir else base_dir / "docs" / "card-creator"
    font_path = Path(fonts_dir) if fonts_dir else None
    fonts = FontSet(custom_dir=font_path)
    logos = load_logo_images(logos_path)

    front = draw_front(data, resolved_name, photo_image, fonts)
    back = draw_back(data, resolved_name, logos, fonts)

    if side_norm == "front":
        output_img = front
    elif side_norm == "back":
        output_img = back
    else:
        output_img = combine_front_back(front, back)

    final_output = output_path if output_path else f"{nickname}.png"
    output = Path(final_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output_img.convert("RGB").save(output, format="PNG")
    return output


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate Data Skaters player card locally")
    p.add_argument("--nickname", required=True)
    p.add_argument("--number", required=True)
    p.add_argument("--position", required=True)
    p.add_argument("--height", required=True)
    p.add_argument("--hand", required=True)
    p.add_argument("--month", required=True)
    p.add_argument("--goals", required=True)
    p.add_argument(
        "--hot-zone",
        required=True,
        help="Hot zone code: TL, TR, BL, BR, or FH",
    )
    p.add_argument("--accuracy", required=True)
    p.add_argument("--archetype", required=True)
    p.add_argument("--side", default="both", choices=["front", "back", "both"])
    p.add_argument("--name", default=None)
    p.add_argument("--pocketbase-url", default=POCKETBASE_URL)
    p.add_argument("--collection-name", default=COLLECTION_NAME)
    p.add_argument("--logos-dir", default=None)
    p.add_argument("--fonts-dir", default=None)
    p.add_argument("--timeout", type=int, default=20)
    return p


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    out = generate_player_card(
        nickname=args.nickname,
        number=args.number,
        position=args.position,
        height=args.height,
        hand=args.hand,
        month=args.month,
        goals=args.goals,
        hot_zone=args.hot_zone,
        accuracy=args.accuracy,
        archetype=args.archetype,
        side=args.side,
        name=args.name,
        output_path=None,
        pocketbase_url=args.pocketbase_url,
        collection_name=args.collection_name,
        logos_dir=args.logos_dir,
        fonts_dir=args.fonts_dir,
        timeout=args.timeout,
    )
    print(f"Card generated: {out}")


if __name__ == "__main__":
    main()
