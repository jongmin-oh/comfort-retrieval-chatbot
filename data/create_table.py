from app.config import MYSQL_DB_NAME, MYSQL_PASSWORD, MYSQL_URL, MYSQL_PORT, MYSQL_USER
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import datetime
import os
import sys

sys.path.insert(1, os.path.abspath('.'))


connection_str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_URL}:{MYSQL_PORT}/{MYSQL_DB_NAME}?charset=utf8mb4"


class ChatBotTable:
    def __init__(self):
        self.DATA_TABLE_NAME = "chatbot_data"
        self.Base = declarative_base()
        self.engine = create_engine(connection_str)

    def drop_chatbot_table(self):
        meta = MetaData()
        meta.reflect(bind=self.engine)
        try:
            table = meta.tables[self.TABLE_NAME]
        except KeyError:
            table = None

        if table is not None:
            self.Base.metadata.drop_all(self.engine, [table], checkfirst=True)

    def create_chatbot_table(self):
        meta = MetaData()
        chatbot_data = Table(
            self.DATA_TABLE_NAME, meta,
            Column('index', Integer, primary_key=True,
                   unique=True, autoincrement=True),
            Column('user', String(512)),
            Column('system', String(512)),
            Column('sentiment', String(15)),
        )
        meta.create_all(self.engine)


chatbot_table = ChatBotTable()
