import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

X_API_KEY = os.getenv("X_API_KEY")

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

PORT = int(os.getenv("PORT", "8080"))
