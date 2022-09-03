import json
from pathlib import Path
from typing import Optional
from webbrowser import get


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


MYSQL_USER = get_secret("MYSQL_USER")
MYSQL_PASSWORD = get_secret("MYSQL_PASSWORD")
MYSQL_DB_NAME = get_secret("MYSQL_DB_NAME")
MYSQL_URL = get_secret("MYSQL_URL")
MYSQL_PORT = get_secret("MYSQL_PORT")

if __name__ == "__main__":
    pass