from create_table import chatbot_table
import pandas as pd
from tqdm import tqdm
from app.models.chatbot_data import ComfortChatData
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.abspath('.'))


BASE_DIR = Path(__file__).resolve().parent


df = pd.read_excel(str(BASE_DIR) + "/base_datasets.xlsx")
df['system']

chatbot_table.drop_chatbot_table()
chatbot_table.create_chatbot_table()

engine = chatbot_table.engine
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()

data = []
for idx, row in tqdm(df.iterrows()):
    data.append(dict(row))

    if idx % 10000 == 0:
        session.bulk_insert_mappings(ComfortChatData, data)
        session.commit()
        data = []

# #20000개 이하 나머지 데이터
session.bulk_insert_mappings(ComfortChatData, data)
session.commit()
session.close()
sys.path.insert(1, os.path.abspath('.'))


BASE_DIR = Path(__file__).resolve().parent


df = pd.read_excel(str(BASE_DIR) + "/base_datasets.xlsx")
df['system']

chatbot_table.drop_chatbot_table()
chatbot_table.create_chatbot_table()

engine = chatbot_table.engine
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()

data = []
for idx, row in tqdm(df.iterrows()):
    data.append(dict(row))

    if idx % 10000 == 0:
        session.bulk_insert_mappings(ComfortChatData, data)
        session.commit()
        data = []

# #20000개 이하 나머지 데이터
session.bulk_insert_mappings(ComfortChatData, data)
session.commit()
session.close()
