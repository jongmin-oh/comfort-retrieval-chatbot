from odmantic import Model
from datetime import datetime

from typing import Optional

class ComfortChatLog(Model):
    query: str
    answer: str
    datetime: datetime 
    distance: Optional[float] 
    answer_type: Optional[str]

    class Config:
        collection = "chat_logs"