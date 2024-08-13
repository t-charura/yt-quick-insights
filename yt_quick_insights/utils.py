import os
import re
from pathlib import Path

import yaml

PROJECT_DIR = Path(__file__).resolve().parent


def load_yaml_file(file_name: str) -> dict:
    """
    Load a YAML file.

    Args:
        file_name: The name of the YAML file

    Returns:
        The content of the YAML file as a dictionary
    """
    yml_file = os.path.join(PROJECT_DIR / "data" / file_name)
    with open(yml_file, "r") as f:
        yml_content = yaml.safe_load(f)

    return yml_content


def clean_youtube_title(video_title: str) -> str:
    """
    Remove unwanted characters from the YouTube video title, because the title is used as a filename.

    Args:
        video_title: The title of the YouTube video

    Returns:
        The cleaned video title
    """
    allowed_chars = re.sub(r"[^a-z0-9 ]", "", video_title.lower()).strip()
    return re.sub(r"\s+", " ", allowed_chars).replace(" ", "_")[0:200]
