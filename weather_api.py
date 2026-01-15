# -*- coding: utf-8 -*-
"""Open-Meteo API client for weather data."""

from __future__ import annotations
import time
import requests

# API endpoint
API_URL = "https://api.open-meteo.com/v1/forecast"

# Cache settings
_cache = {}
_cache_time = 0
CACHE_DURATION = 900  # 15 minutes in seconds


# WMO weather code descriptions
WMO_DESCRIPTIONS = {
    0: "Clear",
    1: "Mostly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime Fog",
    51: "Light Drizzle",
    53: "Drizzle",
    55: "Heavy Drizzle",
    56: "Freezing Drizzle",
    57: "Heavy Freezing Drizzle",
    61: "Light Rain",
    63: "Rain",
    65: "Heavy Rain",
    66: "Freezing Rain",
    67: "Heavy Freezing Rain",
    71: "Light Snow",
    73: "Snow",
    75: "Heavy Snow",
    77: "Snow Grains",
    80: "Light Showers",
    81: "Showers",
    82: "Heavy Showers",
    85: "Light Snow Showers",
    86: "Snow Showers",
    95: "Thunderstorm",
    96: "Thunderstorm w/ Hail",
    99: "Heavy Thunderstorm",
}


def get_weather_description(code):
    """Get human-readable description for WMO weather code."""
    return WMO_DESCRIPTIONS.get(code, "Unknown")


def fetch_weather(latitude, longitude, use_cache=True):
    """
    Fetch weather data from Open-Meteo API.

    Args:
        latitude: Location latitude
        longitude: Location longitude
        use_cache: Whether to use cached data if available

    Returns:
        dict with keys:
            - current: dict with temperature, weather_code, humidity, wind_speed
            - hourly: list of dicts for remaining hours today
            - daily: list of dicts for next 3 days (today, tomorrow, day after)
    """
    global _cache, _cache_time

    cache_key = (latitude, longitude)

    # Check cache
    if use_cache and cache_key in _cache:
        if time.time() - _cache_time < CACHE_DURATION:
            return _cache[cache_key]

    # Build API request
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "hourly": "temperature_2m,weather_code",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
        "forecast_days": 3,
    }

    try:
        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        # If we have cached data, return it even if expired
        if cache_key in _cache:
            return _cache[cache_key]
        raise RuntimeError("Failed to fetch weather data: {}".format(e))

    # Parse current weather
    current = {
        "temperature": data["current"]["temperature_2m"],
        "weather_code": data["current"]["weather_code"],
        "humidity": data["current"]["relative_humidity_2m"],
        "wind_speed": data["current"]["wind_speed_10m"],
        "description": get_weather_description(data["current"]["weather_code"]),
    }

    # Parse hourly data (remaining hours today)
    hourly = []
    hourly_times = data["hourly"]["time"]
    hourly_temps = data["hourly"]["temperature_2m"]
    hourly_codes = data["hourly"]["weather_code"]

    current_hour = time.localtime().tm_hour
    for i, t in enumerate(hourly_times):
        # Parse hour from ISO format "2024-01-15T14:00"
        hour = int(t.split("T")[1].split(":")[0])
        day_index = i // 24

        # Only include remaining hours of today
        if day_index == 0 and hour > current_hour:
            hourly.append({
                "hour": hour,
                "temperature": hourly_temps[i],
                "weather_code": hourly_codes[i],
            })

    # Parse daily forecast
    daily = []
    daily_codes = data["daily"]["weather_code"]
    daily_max = data["daily"]["temperature_2m_max"]
    daily_min = data["daily"]["temperature_2m_min"]
    daily_dates = data["daily"]["time"]

    for i in range(min(3, len(daily_codes))):
        daily.append({
            "date": daily_dates[i],
            "weather_code": daily_codes[i],
            "temp_max": daily_max[i],
            "temp_min": daily_min[i],
            "description": get_weather_description(daily_codes[i]),
        })

    result = {
        "current": current,
        "hourly": hourly,
        "daily": daily,
    }

    # Update cache
    _cache[cache_key] = result
    _cache_time = time.time()

    return result


def get_location_name(latitude, longitude):
    """
    Get location name from coordinates using Open-Meteo geocoding.

    Returns city name or None if lookup fails.
    """
    try:
        # Reverse geocoding via Open-Meteo
        url = "https://geocoding-api.open-meteo.com/v1/search"
        # This is forward geocoding, reverse isn't directly supported
        # For now, just return None and let caller use coordinates
        return None
    except Exception:
        return None


def geocode_location(name):
    """
    Get coordinates for a location name.

    Args:
        name: City name to search for

    Returns:
        tuple (latitude, longitude) or None if not found
    """
    try:
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {"name": name, "count": 1}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return (result["latitude"], result["longitude"])
        return None
    except requests.RequestException:
        return None
