from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, BaseModel

THREADHOLD: float = 0.5
TOP_K: int = 5
EMBED_WEIGHT: float = 0.6
KEYWORD_WEIGHT: float = 0.4
EVASION_ANSWER = "헤헤...무슨말씀이시죠?"

class MainPath(BaseModel):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR.joinpath("resources")
    FAISS_DIR: Path = BASE_DIR.joinpath("models", "faiss")
    BM25_DIR: Path = BASE_DIR.joinpath("models", "bm25")
    MODEL_DIR: Path = BASE_DIR.joinpath("models", "onnx")
    LOGS_DIR: Path = BASE_DIR.joinpath("logs")


class MainConfig(BaseSettings):
    # environment specific variables do not need the Field class
    HOST: Optional[str] = None
    PORT: Optional[int] = None
    LOG_LEVEL: Optional[str] = None

    class Config:
        env_file: str = ".env"


paths = MainPath()
settings = MainConfig()
