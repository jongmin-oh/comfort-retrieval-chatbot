from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os
import sys

sys.path.insert(1, os.path.abspath('.'))

from app.config import MYSQL_DB_NAME, MYSQL_PASSWORD, MYSQL_URL, MYSQL_PORT, MYSQL_USER

connection_str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_URL}:{MYSQL_PORT}/{MYSQL_DB_NAME}?charset=utf8mb4"

class ComfortTable:
    def __init__(self):
        self.TABLE_NAME = "comfort"
        self.Base = declarative_base()
        self.engine = create_engine(connection_str)

    def drop_combot_table(self):
        meta = MetaData()
        meta.reflect(bind=self.engine)
        try:
            table = meta.tables[self.TABLE_NAME]
        except KeyError:
            table = None
        
        if table is not None:
            self.Base.metadata.drop_all(self.engine, [table], checkfirst=True)

    def create_combot_table(self):
        meta = MetaData()
        comfort = Table(
            self.TABLE_NAME, meta,
            Column('index', Integer, primary_key=True, unique=True, autoincrement=True),
            Column('user', String(512)),
            Column('system', String(512)),
            Column('sentiment', String(15)),
        )
        meta.create_all(self.engine)
        
comfort_table = ComfortTable()