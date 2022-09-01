from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import chatbot_answer
from kakao_api import KakaoTemplate
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

skillTemplate = KakaoTemplate()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ComportbotRequest(BaseModel):
    userRequest: str


@app.post("/chatbot")
async def chatbotAPI(request: ComportbotRequest):
    try:
        query = str(request.userRequest['utterance'])
        app.logger.info(f"input query : {str(query)}")
        result = chatbot_answer(query)
        return skillTemplate.send_response(result)
    except Exception as e:
        result = f"에러 : {e}"
        app.logger.info(f"error : {e}")
        return skillTemplate.send_response(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
