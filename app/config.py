# configs.py
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, BaseModel


class MainPath(BaseModel):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR.joinpath("data")
    FAISS_DIR: Path = BASE_DIR.joinpath("models", "faiss")
    MODEL_DIR: Path = BASE_DIR.joinpath("models", "onnx")
    LOGS_DIR: Path = BASE_DIR.joinpath("logs")
    PROMPT_DIR: Path = BASE_DIR.joinpath("data", "prompts")


class MainConfig(BaseSettings):
    # environment specific variables do not need the Field class
    HOST: Optional[str] = None
    PORT: Optional[int] = None
    LOG_LEVEL: Optional[str] = None

    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_NAME: Optional[str] = None

    class Config:
        env_file: str = ".env"


class OpenAiConfig(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None

    class Config:
        env_file: str = ".env"


class ClovaConfig(BaseSettings):
    CLOVA_HOST: Optional[str] = None
    CLOVA_API_KEY: Optional[str] = None
    CLOVA_API_PRIVATE_KEY: Optional[str] = None
    CLOVA_REQUEST_ID: Optional[str] = None

    class Config:
        env_file: str = ".env"


paths = MainPath()
settings = MainConfig()
openai_settings = OpenAiConfig()
clova_settings = ClovaConfig()
