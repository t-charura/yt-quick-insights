from pathlib import Path
from typing import Optional, List

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_DIR = Path.home() / ".insights"


class Settings(BaseSettings):
    # OPENAI settings
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL_NAME: str = "gpt-4o"

    PROJECT_DIR: Path = Path(__file__).resolve().parent
    HOME_DIR: Path = Path.home()

    DEFAULT_LANGUAGES: List[str] = ["en", "de", "es", "fr"]

    model_config = SettingsConfigDict(env_file=ENV_DIR / ".env")


settings = Settings()
