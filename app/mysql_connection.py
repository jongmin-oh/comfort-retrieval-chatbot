import mysql.connector.pooling
from app.config import MYSQL_DB_NAME , MYSQL_PORT , MYSQL_USER , MYSQL_PASSWORD , MYSQL_URL

#MySQL DB 연결
dbconfig = {
    "host" : MYSQL_URL,
    "port" : MYSQL_PORT,
    "user" : MYSQL_USER,
    "passwd": MYSQL_PASSWORD,
    "db": MYSQL_DB_NAME,
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = 'mypool',
                                                      pool_size = 3,
                                                      pool_reset_session=True,
                                                      **dbconfig)

