import os
from pathlib import Path
from typing import Optional, List

from pydantic_settings import BaseSettings, SettingsConfigDict

# TODO: why is this here and not in the Settings class?
ENV_DIR = Path.home() / ".insights"


class Settings(BaseSettings):
    # OPENAI settings
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL_NAME: str = "gpt-4o-mini"

    PROJECT_DIR: Path = Path(__file__).resolve().parent
    HOME_DIR: Path = Path.home()

    STREAMLIT_APP: Path = PROJECT_DIR / "frontend" / "streamlit_app.py"

    MAX_TOKENS: int = 25_000

    DEFAULT_LANGUAGES: List[str] = [
        "en",
        "es",
        "fr",
        "ru",
        "pt",
        "de",
        "it",
        "tr",
        "pl",
        "nl",
    ]

    model_config = SettingsConfigDict(env_file=ENV_DIR / ".env")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.OPENAI_API_KEY is None:
            self.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


settings = Settings()
