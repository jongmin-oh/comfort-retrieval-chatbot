# gunicorn.conf.py
import os
from dotenv import load_dotenv

load_dotenv()

if not os.path.exists("logs"):
    os.makedirs("logs")
    os.makedirs("logs/gunicorn")


host = os.getenv("HOST")
port = os.getenv("PORT")

bind = f"{host}:{port}"
workers = int(os.getenv("N_WORKERS"))
worker_class = "uvicorn.workers.UvicornWorker"
reload = True
# accesslog = "./logs/gunicorn/access.log"
errorlog = "./logs/gunicorn/error.log"
loglevel = "info"
