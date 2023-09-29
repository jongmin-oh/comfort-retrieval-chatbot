from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, BaseModel


class Parms:
    THREADHOLD: float = 0.8
    TOP_K: int = 5
    EVASION_ANSWER = "헤헤...무슨말씀이시죠?"


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

    class Config:
        env_file: str = ".env"


paths = MainPath()
settings = MainConfig()
