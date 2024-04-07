import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("HOST")
port = os.getenv("PORT")

bind = f"{host}:{port}"
workers = int(os.getenv("N_WORKERS"))
worker_class = "uvicorn.workers.UvicornWorker"
reload = True
loglevel = os.getenv("LOG_LEVEL")
