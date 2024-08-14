from pathlib import Path


class Settings:

    PROJECT_DIR = Path(__file__).resolve().parent
    HOME_DIR = Path.home()

    DEFAULT_LANGUAGES = ["en", "de", "es", "fr"]


settings = Settings()
