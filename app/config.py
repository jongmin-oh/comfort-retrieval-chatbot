import json
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent


def get_secret(
    key: str,
    default_value: Optional[str] = None,
    json_path: str = str(BASE_DIR / "secrets.json"),
):
    with open(json_path) as f:
        secrets = json.loads(f.read())
    try:
        return secrets[key]
    except KeyError:
        if default_value:
            return default_value
        raise EnvironmentError(f"Set the {key} environment variable.")


ELASTIC_HOST = get_secret("ELASTIC_HOST")
PINGPONG_API_KEY = get_secret("PINGPONG_KEY")
PINGPONG_URL = get_secret("PINGPONG_URL")
INDEX_NAME = 'chatbot'

if __name__ == "__main__":
    pass