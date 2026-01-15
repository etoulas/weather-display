# -*- coding: utf-8 -*-
"""Weather icons as pixel art for LED matrix display."""

from __future__ import annotations
from PIL import Image, ImageDraw

# Color palette
YELLOW = (255, 200, 0)
ORANGE = (255, 140, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
DARK_GRAY = (80, 80, 80)
BLUE = (0, 150, 255)
LIGHT_BLUE = (100, 200, 255)
BLACK = (0, 0, 0)


def draw_sun_32(img, offset_x=0, offset_y=0):
    """Draw a 32x32 sun icon."""
    draw = ImageDraw.Draw(img)
    cx, cy = 16 + offset_x, 16 + offset_y

    # Sun rays
    ray_color = ORANGE
    # Top
    draw.line([(cx, cy - 14), (cx, cy - 10)], fill=ray_color, width=2)
    # Bottom
    draw.line([(cx, cy + 10), (cx, cy + 14)], fill=ray_color, width=2)
    # Left
    draw.line([(cx - 14, cy), (cx - 10, cy)], fill=ray_color, width=2)
    # Right
    draw.line([(cx + 10, cy), (cx + 14, cy)], fill=ray_color, width=2)
    # Diagonals
    draw.line([(cx - 10, cy - 10), (cx - 7, cy - 7)], fill=ray_color, width=2)
    draw.line([(cx + 7, cy - 7), (cx + 10, cy - 10)], fill=ray_color, width=2)
    draw.line([(cx - 10, cy + 10), (cx - 7, cy + 7)], fill=ray_color, width=2)
    draw.line([(cx + 7, cy + 7), (cx + 10, cy + 10)], fill=ray_color, width=2)

    # Sun circle
    draw.ellipse([(cx - 8, cy - 8), (cx + 8, cy + 8)], fill=YELLOW)


def draw_sun_16(img, offset_x=0, offset_y=0):
    """Draw a 16x16 sun icon."""
    draw = ImageDraw.Draw(img)
    cx, cy = 8 + offset_x, 8 + offset_y

    # Sun rays
    ray_color = ORANGE
    draw.line([(cx, cy - 7), (cx, cy - 5)], fill=ray_color)
    draw.line([(cx, cy + 5), (cx, cy + 7)], fill=ray_color)
    draw.line([(cx - 7, cy), (cx - 5, cy)], fill=ray_color)
    draw.line([(cx + 5, cy), (cx + 7, cy)], fill=ray_color)
    draw.line([(cx - 5, cy - 5), (cx - 3, cy - 3)], fill=ray_color)
    draw.line([(cx + 3, cy - 3), (cx + 5, cy - 5)], fill=ray_color)
    draw.line([(cx - 5, cy + 5), (cx - 3, cy + 3)], fill=ray_color)
    draw.line([(cx + 3, cy + 3), (cx + 5, cy + 5)], fill=ray_color)

    # Sun circle
    draw.ellipse([(cx - 4, cy - 4), (cx + 4, cy + 4)], fill=YELLOW)


def draw_cloud_32(img, offset_x=0, offset_y=0, color=WHITE):
    """Draw a 32x32 cloud icon."""
    draw = ImageDraw.Draw(img)
    ox, oy = offset_x, offset_y

    # Cloud puffs (overlapping circles)
    draw.ellipse([(4 + ox, 12 + oy), (16 + ox, 24 + oy)], fill=color)
    draw.ellipse([(10 + ox, 8 + oy), (24 + ox, 22 + oy)], fill=color)
    draw.ellipse([(18 + ox, 10 + oy), (30 + ox, 22 + oy)], fill=color)
    draw.ellipse([(8 + ox, 14 + oy), (26 + ox, 26 + oy)], fill=color)


def draw_cloud_16(img, offset_x=0, offset_y=0, color=WHITE):
    """Draw a 16x16 cloud icon."""
    draw = ImageDraw.Draw(img)
    ox, oy = offset_x, offset_y

    # Cloud puffs
    draw.ellipse([(2 + ox, 6 + oy), (8 + ox, 12 + oy)], fill=color)
    draw.ellipse([(5 + ox, 4 + oy), (12 + ox, 11 + oy)], fill=color)
    draw.ellipse([(9 + ox, 5 + oy), (15 + ox, 11 + oy)], fill=color)
    draw.ellipse([(4 + ox, 7 + oy), (13 + ox, 13 + oy)], fill=color)


def draw_partly_cloudy_32(img, offset_x=0, offset_y=0):
    """Draw a 32x32 partly cloudy icon (sun behind cloud)."""
    # Sun in upper right
    draw = ImageDraw.Draw(img)
    cx, cy = 24 + offset_x, 10 + offset_y

    # Sun rays (partial)
    draw.line([(cx, cy - 8), (cx, cy - 5)], fill=ORANGE, width=2)
    draw.line([(cx + 5, cy), (cx + 7, cy)], fill=ORANGE, width=2)
    draw.line([(cx + 4, cy - 4), (cx + 6, cy - 6)], fill=ORANGE, width=2)
    draw.ellipse([(cx - 5, cy - 5), (cx + 5, cy + 5)], fill=YELLOW)

    # Cloud in front
    draw_cloud_32(img, offset_x - 2, offset_y + 4, WHITE)


def draw_partly_cloudy_16(img, offset_x=0, offset_y=0):
    """Draw a 16x16 partly cloudy icon."""
    draw = ImageDraw.Draw(img)
    cx, cy = 12 + offset_x, 5 + offset_y

    # Small sun
    draw.line([(cx, cy - 4), (cx, cy - 2)], fill=ORANGE)
    draw.line([(cx + 2, cy), (cx + 4, cy)], fill=ORANGE)
    draw.ellipse([(cx - 2, cy - 2), (cx + 2, cy + 2)], fill=YELLOW)

    # Cloud in front
    draw_cloud_16(img, offset_x - 1, offset_y + 2, WHITE)


def draw_rain_32(img, offset_x=0, offset_y=0, heavy=False):
    """Draw a 32x32 rain icon."""
    draw = ImageDraw.Draw(img)
    ox, oy = offset_x, offset_y

    # Cloud
    draw_cloud_32(img, ox, oy - 4, GRAY)

    # Rain drops
    drop_color = BLUE
    drops_x = [8, 16, 24] if not heavy else [6, 11, 16, 21, 26]
    for dx in drops_x:
        draw.line([(dx + ox, 24 + oy), (dx + ox - 2, 30 + oy)], fill=drop_color, width=2)

    if heavy:
        for dx in [8, 14, 20]:
            draw.line([(dx + ox, 28 + oy), (dx + ox - 2, 32 + oy)], fill=drop_color, width=2)


def draw_rain_16(img, offset_x=0, offset_y=0, heavy=False):
    """Draw a 16x16 rain icon."""
    draw = ImageDraw.Draw(img)
    ox, oy = offset_x, offset_y

    # Cloud
    draw_cloud_16(img, ox, oy - 2, GRAY)

    # Rain drops
    drop_color = BLUE
    drops_x = [4, 8, 12] if not heavy else [3, 6, 9, 12]
    for dx in drops_x:
        draw.line([(dx + ox, 12 + oy), (dx + ox - 1, 15 + oy)], fill=drop_color)


def draw_snow_32(img, offset_x=0, offset_y=0):
    """Draw a 32x32 snow icon."""
    draw = ImageDraw.Draw(img)
    ox, oy = offset_x, offset_y

    # Cloud
    draw_cloud_32(img, ox, oy - 4, GRAY)

    # Snowflakes (asterisks)
    snow_color = LIGHT_BLUE
    for sx, sy in [(8, 26), (16, 28), (24, 25), (12, 30), (20, 31)]:
        x, y = sx + ox, sy + oy
        # Simple snowflake
        draw.point((x, y), fill=snow_color)
        draw.point((x - 1, y), fill=snow_color)
        draw.point((x + 1, y), fill=snow_color)
        draw.point((x, y - 1), fill=snow_color)
        draw.point((x, y + 1), fill=snow_color)


def draw_snow_16(img, offset_x=0, offset_y=0):
    """Draw a 16x16 snow icon."""
    draw = ImageDraw.Draw(img)
    ox, oy = offset_x, offset_y

    # Cloud
    draw_cloud_16(img, ox, oy - 2, GRAY)

    # Snowflakes (dots)
    snow_color = LIGHT_BLUE
    for sx, sy in [(4, 13), (8, 14), (12, 13), (6, 15), (10, 15)]:
        draw.point((sx + ox, sy + oy), fill=snow_color)


def draw_thunder_32(img, offset_x=0, offset_y=0):
    """Draw a 32x32 thunderstorm icon."""
    draw = ImageDraw.Draw(img)
    ox, oy = offset_x, offset_y

    # Dark cloud
    draw_cloud_32(img, ox, oy - 4, DARK_GRAY)

    # Lightning bolt
    bolt = [
        (16 + ox, 18 + oy),
        (14 + ox, 24 + oy),
        (17 + ox, 24 + oy),
        (13 + ox, 32 + oy),
        (20 + ox, 22 + oy),
        (17 + ox, 22 + oy),
        (19 + ox, 18 + oy),
    ]
    draw.polygon(bolt, fill=YELLOW)

    # Rain drops
    draw.line([(8 + ox, 24 + oy), (6 + ox, 30 + oy)], fill=BLUE, width=2)
    draw.line([(24 + ox, 24 + oy), (22 + ox, 30 + oy)], fill=BLUE, width=2)


def draw_thunder_16(img, offset_x=0, offset_y=0):
    """Draw a 16x16 thunderstorm icon."""
    draw = ImageDraw.Draw(img)
    ox, oy = offset_x, offset_y

    # Dark cloud
    draw_cloud_16(img, ox, oy - 2, DARK_GRAY)

    # Lightning bolt
    bolt = [
        (8 + ox, 10 + oy),
        (6 + ox, 13 + oy),
        (8 + ox, 13 + oy),
        (6 + ox, 16 + oy),
        (10 + ox, 12 + oy),
        (8 + ox, 12 + oy),
        (9 + ox, 10 + oy),
    ]
    draw.polygon(bolt, fill=YELLOW)


def draw_fog_32(img, offset_x=0, offset_y=0):
    """Draw a 32x32 fog icon."""
    draw = ImageDraw.Draw(img)
    ox, oy = offset_x, offset_y

    # Horizontal fog lines
    fog_color = GRAY
    for y_off in [10, 16, 22, 28]:
        # Varying line lengths for effect
        x_start = 4 if y_off in [10, 22] else 8
        x_end = 28 if y_off in [16, 28] else 24
        draw.line([(x_start + ox, y_off + oy), (x_end + ox, y_off + oy)],
                  fill=fog_color, width=2)


def draw_fog_16(img, offset_x=0, offset_y=0):
    """Draw a 16x16 fog icon."""
    draw = ImageDraw.Draw(img)
    ox, oy = offset_x, offset_y

    # Horizontal fog lines
    fog_color = GRAY
    for y_off in [5, 8, 11, 14]:
        x_start = 2 if y_off in [5, 11] else 4
        x_end = 14 if y_off in [8, 14] else 12
        draw.line([(x_start + ox, y_off + oy), (x_end + ox, y_off + oy)], fill=fog_color)


# Icon type constants
ICON_SUN = 'sun'
ICON_PARTLY_CLOUDY = 'partly_cloudy'
ICON_CLOUDY = 'cloudy'
ICON_RAIN = 'rain'
ICON_HEAVY_RAIN = 'heavy_rain'
ICON_SNOW = 'snow'
ICON_THUNDER = 'thunder'
ICON_FOG = 'fog'


def get_icon_32(icon_type):
    """Get a 32x32 weather icon as a PIL Image."""
    img = Image.new('RGB', (32, 32), BLACK)

    if icon_type == ICON_SUN:
        draw_sun_32(img)
    elif icon_type == ICON_PARTLY_CLOUDY:
        draw_partly_cloudy_32(img)
    elif icon_type == ICON_CLOUDY:
        draw_cloud_32(img, 0, 4, GRAY)
    elif icon_type == ICON_RAIN:
        draw_rain_32(img)
    elif icon_type == ICON_HEAVY_RAIN:
        draw_rain_32(img, heavy=True)
    elif icon_type == ICON_SNOW:
        draw_snow_32(img)
    elif icon_type == ICON_THUNDER:
        draw_thunder_32(img)
    elif icon_type == ICON_FOG:
        draw_fog_32(img)
    else:
        # Default: question mark or empty
        draw_cloud_32(img, 0, 4, DARK_GRAY)

    return img


def get_icon_16(icon_type):
    """Get a 16x16 weather icon as a PIL Image."""
    img = Image.new('RGB', (16, 16), BLACK)

    if icon_type == ICON_SUN:
        draw_sun_16(img)
    elif icon_type == ICON_PARTLY_CLOUDY:
        draw_partly_cloudy_16(img)
    elif icon_type == ICON_CLOUDY:
        draw_cloud_16(img, 0, 2, GRAY)
    elif icon_type == ICON_RAIN:
        draw_rain_16(img)
    elif icon_type == ICON_HEAVY_RAIN:
        draw_rain_16(img, heavy=True)
    elif icon_type == ICON_SNOW:
        draw_snow_16(img)
    elif icon_type == ICON_THUNDER:
        draw_thunder_16(img)
    elif icon_type == ICON_FOG:
        draw_fog_16(img)
    else:
        draw_cloud_16(img, 0, 2, DARK_GRAY)

    return img


def wmo_code_to_icon(code):
    """Map WMO weather code to icon type."""
    if code == 0:
        return ICON_SUN
    elif code in (1, 2, 3):
        return ICON_PARTLY_CLOUDY if code <= 2 else ICON_CLOUDY
    elif code in (45, 48):
        return ICON_FOG
    elif code in (51, 53, 55, 56, 57):
        return ICON_RAIN  # Drizzle
    elif code in (61, 63, 80, 81):
        return ICON_RAIN
    elif code in (65, 66, 67, 82):
        return ICON_HEAVY_RAIN
    elif code in (71, 73, 75, 77, 85, 86):
        return ICON_SNOW
    elif code in (95, 96, 99):
        return ICON_THUNDER
    else:
        return ICON_CLOUDY  # Default fallback
