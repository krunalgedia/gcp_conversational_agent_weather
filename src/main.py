from fastapi import Depends, FastAPI
from pydantic import BaseModel

from src.utils import get_weather, verify_token
from src import logging

app = FastAPI(title="Weather APIs for the Google Conversational Agents.", version="0.1.0")


logger = logging.getLogger(__name__)


class PlaybookRequest(BaseModel):
    city: str


@app.post("/weather", response_model=None)
async def handle_post_weather(
    playbook_request: PlaybookRequest, is_valid: bool = Depends(verify_token)
):
    try:
        return await get_weather(city=playbook_request.city)
    except Exception as e:
        logger.info("Error at handle_post_weather:")
        logger.error(e)
        return {
            "status": "FAILURE",
            "message": "Due to a technical issue unable to get the weather updates.",
        }
