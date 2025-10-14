from fastapi import Depends, FastAPI
from pydantic import BaseModel

from src.utils import get_weather, verify_token
from src import logging

app = FastAPI(title="Wanerby Geocoding API", version="0.1.0")


logger = logging.getLogger(__name__)


class PlaybookRequest(BaseModel):
    city: str


@app.post("/weather", response_model=None)
async def handle_post_weather(
    playbook_request: PlaybookRequest, is_valid: bool = Depends(verify_token)
):
    try:
        return await get_weather(city=playbook_request.city)
        # return {
        #     "city": f"{playbook_request.city}",
        #     "temperature": "25 degree",
        #     "feels_like": "Good",
        #     "humidity": "No humidity",
        #     "pressure": "No pressure",
        #     "clouds": "No clouds, clear sky",
        # }
    except Exception as e:
        logger.info("Error at handle_post_high_priority_sos:")
        logger.error(e)
        return {
            "status": "FAILURE",
            "message": "Due to a technical issue unable to get the weather updates.",
        }
