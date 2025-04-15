import os
from pathlib import Path
from typing import Optional, List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # OPENAI settings
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL_NAME: str = "gpt-4.1-mini"

    # Directories
    PROJECT_DIR: Path = Path(__file__).resolve().parent
    HOME_DIR: Path = Path.home()
    LOCAL_CONFIG_DIR: Path = HOME_DIR / ".insights"

    # Application Entry Point
    STREAMLIT_APP: Path = PROJECT_DIR / "frontend" / "streamlit_app.py"
    STYLES_CSS: Path = PROJECT_DIR / "frontend" / "static" / "styles.css"

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

    model_config = SettingsConfigDict(env_file=LOCAL_CONFIG_DIR / ".env")

    # Load OPENAI_API_KEY from environment variable if not set in the .env file
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.OPENAI_API_KEY is None:
            self.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


settings = Settings()
