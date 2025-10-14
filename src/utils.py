from typing import Optional, Dict

from fastapi.requests import Request
from fastapi import HTTPException, status
import aiohttp

from src import config


async def verify_token(request: Request) -> bool:
    x_api_key = request.headers.get("X-API-Key")

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid X-API-Key header",
        )

    if x_api_key != config.X_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid X-API-Key",
        )
    return True


async def get_weather(
    city: str,
    units: str = "metric",  # metric, imperial, or standard
) -> Optional[Dict] | None:
    """
    Fetch weather data from OpenWeatherMap API asynchronously.

    Args:
        city: City name (e.g., "London" or "London,UK")
        units: Temperature units - "metric" (Celsius), "imperial" (Fahrenheit), or "standard" (Kelvin)

    Returns:
        Dictionary containing weather data or None if request fails
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": config.OPENWEATHERMAP_API_KEY, "units": units}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "city": data["name"],
                        "country": data["sys"]["country"],
                        "temperature": data["main"]["temp"],
                        "feels_like": data["main"]["feels_like"],
                        "humidity": data["main"]["humidity"],
                        "pressure": data["main"]["pressure"],
                        "weather": data["weather"][0]["description"],
                        "wind_speed": data["wind"]["speed"],
                        "clouds": data["clouds"]["all"],
                    }
                else:
                    print(f"Error: {response.status} - {await response.text()}")
                    return None
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return None
