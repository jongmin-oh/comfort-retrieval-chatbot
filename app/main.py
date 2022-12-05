from typing import Dict
from fastapi import FastAPI
from app.chatbot import search_reply
from app.kakao_api import skillTemplate
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.connection import elastic
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

class ComportbotRequest(BaseModel):
    userRequest: Dict
    
class testRequest(BaseModel):
    question : str

@app.post("/test")
async def chatbotAPI(request: testRequest):
        query = request.question
        result = search_reply(query)
        return result


@app.post("/chatbot")
async def chatbotAPI(request: ComportbotRequest):
    try:
        query = request.userRequest['utterance']
        print(request.userRequest)
        result = search_reply(query)
        return skillTemplate.send_response(result)

    except Exception as e:
        result = f"에러 : {e}"
        logger.info(result)
        return skillTemplate.send_response(result)


@app.on_event("startup")
def on_app_start():
    elastic.connect()
    print("hello server")


@app.on_event("shutdown")
def on_app_shutdown():
    elastic.close()
    print("bye server")