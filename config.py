import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    db_path: str
    user_agent: str

REQUIRED_KEYS = ("DB_PATH", "USER_AGENT")

def _load_dotenv(path: str = ".env") -> None:
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

def load_config() -> Config:
    _load_dotenv()
    missing = [key for key in REQUIRED_KEYS if not os.environ.get(key)]
    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")
    return Config(
        db_path=os.environ["DB_PATH"],
        user_agent=os.environ["USER_AGENT"],
    )