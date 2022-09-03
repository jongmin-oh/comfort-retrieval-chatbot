from typing import Optional
from fastapi import FastAPI
from app.chatbot import chatbot_answer
from app.kakao_api import KakaoTemplate
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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
    return {"Hello" : "FastApi"}


class ComportbotRequest(BaseModel):
    userRequest: str


@app.post("/chatbot")
async def chatbotAPI(request: ComportbotRequest):
    try:
        query = request.userRequest
        # app.logger.info(f"input query : {str(query)}")
        result = chatbot_answer(query)
        return skillTemplate.send_response(result)
        
    except Exception as e:
        result = f"에러 : {e}"
        # app.logger.info(f"error : {e}")
        return skillTemplate.send_response(result)