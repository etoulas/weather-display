# Weather Display for 64x64 RGB LED Matrix

## Project Overview
Displays current weather conditions and 3-day forecast on a 64x64 RGB LED matrix panel using the Open-Meteo API.

## Target Hardware
- RGB Matrix P3.0 64x64 (HUB75 interface)
- Raspberry Pi 1 Model B Rev. 2
- Debian 10 (buster), Python 3.7

## Project Structure
```
main.py          - Entry point, CLI argument parsing, main loop
weather_api.py   - Open-Meteo API client with 15-min caching
display.py       - LED matrix rendering using PIL
icons.py         - Weather pixel art (32x32 large, 16x16 small)
requirements.txt - Dependencies (requests, Pillow)
```

## Commands
```bash
# Test without hardware (generates preview.png)
./venv/bin/python main.py --preview

# Run in simulation mode (no LED output)
./venv/bin/python main.py --simulate

# Run on Raspberry Pi (requires sudo for GPIO)
sudo venv/bin/python main.py --location "Uster"
```

## Key Details
- Default location: Uster, Switzerland (47.3472, 8.7203)
- `rgbmatrix` library must be installed separately from hzeller/rpi-rgb-led-matrix (not on PyPI)
- Display layout: top half = current weather (32x32 icon + temp), bottom half = 3-day forecast
- WMO weather codes mapped to icons in `icons.py:wmo_code_to_icon()`
- API responses cached for 15 minutes to reduce load on Pi 1
