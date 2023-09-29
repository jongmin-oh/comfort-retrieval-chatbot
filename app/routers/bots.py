from typing import Dict
import logging

from fastapi import APIRouter

from pydantic import BaseModel
from app.services.chatbot import ComfortBot
from app.services.kakao_api import skillTemplate

router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s:%(message)s",
    level=logging.INFO,
    filename="logs/log.log",
    filemode="w",
)
logger = logging.getLogger(__name__)


class ComfortBotTestRequest(BaseModel):
    query: str


class ComfortbotRequest(BaseModel):
    userRequest: Dict


@router.post("/comfort")
async def comfort(request: ComfortBotTestRequest):
    answer = ComfortBot().reply(request.query)
    return {"A": answer}


@router.post("/kakao")
async def kakao(request: ComfortbotRequest):
    try:
        query = request.userRequest["utterance"]
        result = ComfortBot().reply(query)
        return skillTemplate.send_response(result)

    except Exception as e:
        result = f"에러 : {e}"
        logger.info(result)
        return skillTemplate.send_response(result)
