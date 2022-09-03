from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from tqdm import tqdm
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

from create_table import comfort_table

df = pd.read_excel(str(BASE_DIR) + "/base_datasets.xlsx")
df['system']

comfort_table.drop_combot_table()
comfort_table.create_combot_table()

Base = declarative_base()

class ComfortBaseData(Base):
    __tablename__ = comfort_table.TABLE_NAME

    index = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user = Column(String(512))
    system = Column(String(512))
    sentiment = Column(String(15))


engine = comfort_table.engine
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()

data = []
for idx , row in tqdm(df.iterrows()):
    data.append(dict(row))
    
    if idx % 10000 == 0:
        session.bulk_insert_mappings(ComfortBaseData, data)
        session.commit()
        data = []

# #20000개 이하 나머지 데이터
session.bulk_insert_mappings(ComfortBaseData, data)
session.commit()
session.close()
