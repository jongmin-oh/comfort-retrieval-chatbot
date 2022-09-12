from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

import app.config as config
import mysql.connector.pooling

#MySQL DB 연결
mysql_config = {
    "host" : config.MYSQL_URL,
    "port" : config.MYSQL_PORT,
    "user" : config.MYSQL_USER,
    "passwd": config.MYSQL_PASSWORD,
    "db": config.MYSQL_DB_NAME,
}

class MongoDB:
    def __init__(self):
        self.client = None
        self.engine = None
    
    def connect(self):
        self.client = AsyncIOMotorClient(
                        host=config.MONGODB_URL,
                        username=config.MONGODB_USER,
                        password=config.MONGODB_PASSWORD
                    )
        self.engine = AIOEngine(client=self.client, database=config.MONGODB_DB_NAME)

    def close(self):
        self.client.close()

mongodb = MongoDB()
cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = 'mypool',
                                                      pool_size = 3,
                                                      pool_reset_session=True,
                                                      **mysql_config)