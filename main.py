#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weather Display for 64x64 RGB LED Matrix

Displays current weather conditions and 3-day forecast using Open-Meteo API.
"""

from __future__ import annotations
import argparse
import signal
import sys
import time

from weather_api import fetch_weather, geocode_location
from display import WeatherDisplay, preview_weather

# Default location: Uster, Switzerland
DEFAULT_LAT = 47.3472
DEFAULT_LON = 8.7203
DEFAULT_LOCATION = "Uster, Switzerland"


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Display weather on 64x64 RGB LED matrix",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Use default location (Uster, Switzerland)
  %(prog)s --location "Zurich"       # Look up location by name
  %(prog)s --lat 47.37 --lon 8.54    # Use specific coordinates
  %(prog)s --preview                 # Generate preview image without hardware
        """
    )

    parser.add_argument(
        "--latitude", "--lat",
        type=float,
        default=None,
        help="Location latitude (default: {})".format(DEFAULT_LAT)
    )
    parser.add_argument(
        "--longitude", "--lon",
        type=float,
        default=None,
        help="Location longitude (default: {})".format(DEFAULT_LON)
    )
    parser.add_argument(
        "--location", "-l",
        type=str,
        default=None,
        help="Location name to look up (e.g., 'Zurich', 'New York')"
    )
    parser.add_argument(
        "--brightness", "-b",
        type=int,
        default=50,
        help="LED brightness 0-100 (default: 50)"
    )
    parser.add_argument(
        "--refresh", "-r",
        type=int,
        default=15,
        help="Refresh interval in minutes (default: 15)"
    )
    parser.add_argument(
        "--preview", "-p",
        action="store_true",
        help="Generate preview image and exit (no hardware needed)"
    )
    parser.add_argument(
        "--simulate", "-s",
        action="store_true",
        help="Run without LED hardware (for testing)"
    )

    return parser.parse_args()


def get_coordinates(args):
    """Get latitude and longitude from arguments."""
    # Priority: explicit coords > location name > defaults
    if args.latitude is not None and args.longitude is not None:
        return args.latitude, args.longitude

    if args.location:
        print("Looking up location: {}".format(args.location))
        coords = geocode_location(args.location)
        if coords:
            print("Found: {:.4f}, {:.4f}".format(coords[0], coords[1]))
            return coords
        else:
            print("Location not found, using default")

    return DEFAULT_LAT, DEFAULT_LON


def main():
    """Main entry point."""
    args = parse_args()

    # Get coordinates
    lat, lon = get_coordinates(args)
    print("Weather location: {:.4f}, {:.4f}".format(lat, lon))

    # Preview mode
    if args.preview:
        print("Fetching weather data...")
        weather = fetch_weather(lat, lon)
        print("Current: {}C, {}".format(
            weather["current"]["temperature"],
            weather["current"]["description"]
        ))
        output = preview_weather(weather)
        print("Preview saved to: {}".format(output))
        return 0

    # Initialize display
    print("Initializing display...")
    simulate = args.simulate
    display = WeatherDisplay(brightness=args.brightness, simulate=simulate)

    if simulate:
        print("Running in simulation mode (no hardware)")

    # Handle shutdown gracefully
    running = True

    def signal_handler(sig, frame):
        nonlocal running
        print("\nShutting down...")
        running = False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Main loop
    refresh_seconds = args.refresh * 60
    last_update = 0

    print("Starting weather display (refresh every {} min)".format(args.refresh))
    print("Press Ctrl+C to exit")

    try:
        while running:
            now = time.time()

            # Check if we need to update
            if now - last_update >= refresh_seconds or last_update == 0:
                try:
                    print("Fetching weather data...")
                    weather = fetch_weather(lat, lon)

                    current = weather["current"]
                    print("Current: {:.1f}C, {} (humidity: {}%, wind: {} km/h)".format(
                        current["temperature"],
                        current["description"],
                        current["humidity"],
                        current["wind_speed"]
                    ))

                    print("Rendering to display...")
                    display.render(weather)
                    last_update = now

                except Exception as e:
                    print("Error updating weather: {}".format(e))
                    # Wait a bit before retrying
                    time.sleep(60)
                    continue

            # Sleep until next update or interrupt
            sleep_time = min(60, refresh_seconds - (time.time() - last_update))
            if sleep_time > 0:
                time.sleep(sleep_time)

    finally:
        print("Cleaning up...")
        display.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
