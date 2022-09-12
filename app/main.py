from typing import Optional, Dict
from fastapi import FastAPI
from app.chatbot import chatbot_answer
from app.kakao_api import KakaoTemplate
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.models import mongodb
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

skillTemplate = KakaoTemplate()


@app.get("/")
def read_root():
    return {"Hello": "FastApi"}


class ComportbotRequest(BaseModel):
    userRequest: Dict


@app.post("/chatbot")
async def chatbotAPI(request: ComportbotRequest):
    try:
        query = request.userRequest['utterance']
        # app.logger.info(f"input query : {str(query)}")
        result = chatbot_answer(query)

        mongodb.connect()

        return skillTemplate.send_response(result)

    except Exception as e:
        result = f"에러 : {e}"
        logger.info(result)
        return skillTemplate.send_response(result)


@app.on_event("startup")
def on_app_start():
    print("hello server")


@app.on_event("shutdown")
def on_app_shutdown():
    print("bye server")
