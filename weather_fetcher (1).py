import sys
from datetime import datetime

import requests

API_URL = "https://api.open-meteo.com/v1/forecast"
LOG_FILE = "weather_report.txt"
TIMEOUT_SECONDS = 10
DEFAULT_LATITUDE = 19.0760
DEFAULT_LONGITUDE = 72.8777

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    51: "Drizzle",
    61: "Rain",
    71: "Snow",
    80: "Rain showers",
    95: "Thunderstorm",
}


def get_coordinates():
    if len(sys.argv) == 3:
        try:
            return float(sys.argv[1]), float(sys.argv[2])
        except ValueError:
            print("Invalid coordinates supplied. Using defaults.")
    return DEFAULT_LATITUDE, DEFAULT_LONGITUDE


def fetch_weather(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
        "timezone": "auto",
    }
    try:
        response = requests.get(API_URL, params=params, timeout=TIMEOUT_SECONDS)
        if response.status_code != 200:
            print("Request failed with HTTP status code:", response.status_code)
            return None
        return response.json()
    except requests.exceptions.ConnectTimeout:
        print("Connection timed out while contacting the weather service.")
    except requests.exceptions.ReadTimeout:
        print("The weather service took too long to respond.")
    except requests.exceptions.ConnectionError:
        print("Network connection error. Please check your internet connection.")
    except requests.exceptions.RequestException as error:
        print("Unexpected request error:", error)
    except ValueError:
        print("The response could not be decoded as JSON.")
    return None


def parse_weather(data):
    try:
        current = data["current_weather"]
        return {
            "temperature": current["temperature"],
            "windspeed": current["windspeed"],
            "weathercode": current["weathercode"],
            "timezone": data["timezone"],
        }
    except (KeyError, TypeError):
        print("The response is missing expected weather fields.")
        return None


def describe_weather(code):
    return WEATHER_CODES.get(code, "Unknown conditions")


def build_summary(metrics, latitude, longitude):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    condition = describe_weather(metrics["weathercode"])
    lines = [
        "=" * 44,
        "Weather Report - " + timestamp,
        "=" * 44,
        "Location     : {:.4f}, {:.4f}".format(latitude, longitude),
        "Timezone     : " + str(metrics["timezone"]),
        "Temperature  : {} C".format(metrics["temperature"]),
        "Wind Speed   : {} km/h".format(metrics["windspeed"]),
        "Weather Code : {} ({})".format(metrics["weathercode"], condition),
        "",
    ]
    return "\n".join(lines)


def save_report(summary):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(summary + "\n")
        return True
    except OSError as error:
        print("Could not write to", LOG_FILE + ":", error)
        return False


def main():
    latitude, longitude = get_coordinates()
    data = fetch_weather(latitude, longitude)
    if data is None:
        return
    metrics = parse_weather(data)
    if metrics is None:
        return
    summary = build_summary(metrics, latitude, longitude)
    print(summary)
    if save_report(summary):
        print("Report saved to", LOG_FILE)


if __name__ == "__main__":
    main()
