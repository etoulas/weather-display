# -*- coding: utf-8 -*-
"""LED matrix display renderer for weather data."""

from __future__ import annotations
from PIL import Image, ImageDraw, ImageFont

from icons import get_icon_32, get_icon_16, wmo_code_to_icon

# Display dimensions
WIDTH = 64
HEIGHT = 64

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 220, 100)
CYAN = (100, 220, 255)
GRAY = (120, 120, 120)
BLACK = (0, 0, 0)

# Try to import rgbmatrix, but allow running without it for testing
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    HAS_MATRIX = True
except ImportError:
    HAS_MATRIX = False
    RGBMatrix = None
    RGBMatrixOptions = None


class WeatherDisplay:
    """Renders weather data to an RGB LED matrix."""

    def __init__(self, brightness=50, simulate=False):
        """
        Initialize the display.

        Args:
            brightness: LED brightness (0-100)
            simulate: If True, don't use hardware (for testing)
        """
        self.brightness = brightness
        self.simulate = simulate or not HAS_MATRIX
        self.matrix = None
        self.canvas = None

        if not self.simulate:
            self._init_matrix()

        # Load a small font for temperature display
        # Use PIL's default bitmap font (always available)
        self.font = ImageFont.load_default()

    def _init_matrix(self):
        """Initialize the RGB matrix hardware."""
        options = RGBMatrixOptions()
        options.rows = 64
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.brightness = self.brightness
        options.hardware_mapping = 'regular'

        # Pi 1 specific options for stability
        options.gpio_slowdown = 4  # Slow down GPIO for Pi 1
        options.disable_hardware_pulsing = True  # Avoid PWM conflicts

        self.matrix = RGBMatrix(options=options)
        self.canvas = self.matrix.CreateFrameCanvas()

    def set_brightness(self, brightness):
        """Set display brightness (0-100)."""
        self.brightness = max(0, min(100, brightness))
        if self.matrix:
            self.matrix.brightness = self.brightness

    def render(self, weather_data):
        """
        Render weather data to the display.

        Args:
            weather_data: dict from weather_api.fetch_weather()

        Returns:
            PIL Image (for testing/preview)
        """
        # Create frame image
        img = Image.new('RGB', (WIDTH, HEIGHT), BLACK)
        draw = ImageDraw.Draw(img)

        current = weather_data.get("current", {})
        daily = weather_data.get("daily", [])

        # === Top half: Current weather ===
        # Large icon on left (32x32)
        icon_type = wmo_code_to_icon(current.get("weather_code", 0))
        icon = get_icon_32(icon_type)
        img.paste(icon, (0, 0))

        # Temperature on right (large digits)
        temp = current.get("temperature", 0)
        temp_str = "{:.0f}".format(temp)
        temp_color = self._temp_color(temp)

        # Draw temperature with larger effect using multiple draws
        # Position in upper right area
        self._draw_large_temp(draw, temp_str, 36, 4, temp_color)

        # Degree symbol
        draw.text((56, 4), "o", fill=temp_color, font=self.font)

        # Weather description below temperature (truncated)
        desc = current.get("description", "")[:8]
        draw.text((34, 20), desc, fill=GRAY, font=self.font)

        # === Bottom half: 3-day forecast ===
        # Divider line
        draw.line([(0, 32), (63, 32)], fill=GRAY)

        # Three columns: ~21 pixels each
        col_width = 21
        for i, day in enumerate(daily[:3]):
            x_offset = i * col_width + 2

            # Day label (Today, Tom, +2)
            if i == 0:
                label = "Now"
            elif i == 1:
                label = "Tom"
            else:
                label = "+2d"
            draw.text((x_offset + 2, 34), label, fill=GRAY, font=self.font)

            # Small weather icon (16x16)
            day_icon_type = wmo_code_to_icon(day.get("weather_code", 0))
            day_icon = get_icon_16(day_icon_type)
            img.paste(day_icon, (x_offset + 2, 42))

            # High/low temps
            hi = day.get("temp_max", 0)
            lo = day.get("temp_min", 0)
            hi_str = "{:.0f}".format(hi)
            lo_str = "{:.0f}".format(lo)

            # High temp (warm color)
            draw.text((x_offset, 58), hi_str, fill=self._temp_color(hi), font=self.font)
            # Separator
            draw.text((x_offset + 10, 58), "/", fill=GRAY, font=self.font)
            # Low temp (cool color)
            draw.text((x_offset + 14, 58), lo_str, fill=self._temp_color(lo), font=self.font)

        # Send to matrix
        if not self.simulate and self.matrix:
            self.canvas.SetImage(img)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)

        return img

    def _draw_large_temp(self, draw, temp_str, x, y, color):
        """Draw temperature in a larger/bolder style."""
        # Simple approach: draw text multiple times with slight offsets
        # This creates a bolder appearance on the small display
        for dx in range(2):
            for dy in range(2):
                draw.text((x + dx, y + dy), temp_str, fill=color, font=self.font)

    def _temp_color(self, temp):
        """Get color based on temperature (Celsius)."""
        if temp >= 25:
            return YELLOW  # Hot
        elif temp >= 15:
            return WHITE  # Mild
        elif temp >= 5:
            return CYAN  # Cool
        else:
            return (150, 200, 255)  # Cold (light blue)

    def clear(self):
        """Clear the display."""
        if not self.simulate and self.matrix:
            self.matrix.Clear()

    def close(self):
        """Clean up resources."""
        self.clear()


def preview_weather(weather_data, output_path="preview.png"):
    """
    Generate a preview image without hardware.

    Args:
        weather_data: Weather data dict
        output_path: Where to save the preview image

    Returns:
        Path to saved image
    """
    display = WeatherDisplay(simulate=True)
    img = display.render(weather_data)

    # Scale up for easier viewing (8x)
    preview = img.resize((512, 512), Image.NEAREST)
    preview.save(output_path)

    return output_path
