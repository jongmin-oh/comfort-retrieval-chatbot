from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ComfortChatData(Base):
    __tablename__ = "chatbot_data"

    index = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user = Column(String(512))
    system = Column(String(512))
    sentiment = Column(String(15))

