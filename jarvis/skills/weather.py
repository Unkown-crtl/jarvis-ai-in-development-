import json
import urllib.request

def get_weather_forecast(location: str = "Berlin") -> str:
    """Fetches the current weather and daily forecast for a given location using Open-Meteo."""
    coordinates = {
        "berlin": {"lat": 52.52, "lon": 13.41},
        "london": {"lat": 51.50, "lon": -0.12},
        "new york": {"lat": 40.71, "lon": -74.00},
        "tokyo": {"lat": 35.67, "lon": 139.65},
        "paris": {"lat": 48.85, "lon": 2.35}
    }
    
    loc_key = location.lower().strip()
    geo = coordinates.get(loc_key, coordinates["berlin"])
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={geo['lat']}&longitude={geo['lon']}&current_weather=true&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=auto"
    
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            current = data["current_weather"]
            daily = data["daily"]
            
            temp = current["temperature"]
            wind = current["windspeed"]
            high = daily["temperature_2m_max"][0]
            low = daily["temperature_2m_min"][0]
            code = current["weathercode"]
            
            conditions = "Clear/Cloudy"
            if code >= 51 and code <= 67:
                conditions = "Rainy"
            elif code >= 71 and code <= 86:
                conditions = "Snowy"
            elif code >= 95:
                conditions = "Stormy"
                
            return f"[weather_skill] Current weather in {location.title()}: {temp}°C, {conditions}. Wind speed: {wind} km/h. Forecast for today: High of {high}°C, Low of {low}°C."
    except Exception as e:
        return f"[weather_skill] Error fetching weather data: {str(e)}"


SKILLS = [
    {
        "name": "get_weather_forecast",
        "description": "Fetches current weather conditions and daily temperatures for a specific city.",
        "trigger_phrases": ["weather", "forecast", "temperature", "is it raining", "how cold is it"],
        "func": get_weather_forecast,
    },
]