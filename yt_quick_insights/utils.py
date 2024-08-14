import re

import yaml

from yt_quick_insights.config import settings


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


def load_yaml_file(file_name: str, user_yaml: bool = False) -> dict[str, str]:
    """
    Load a YAML file from either the project directory or the user's home directory

    Args:
        file_name: The name of the YAML file
        user_yaml: If True, load from user's home directory; otherwise, from project directory.

    Returns:
        The content of the YAML file as a dictionary

    Raises:
        yaml.YAMLError: If there is an error parsing the YAML file
    """
    yaml_directory = (
        settings.HOME_DIR / ".insights" if user_yaml else settings.PROJECT_DIR / "data"
    )
    yaml_file = yaml_directory / file_name

    try:
        with open(yaml_file, "r") as file:
            yaml_content = yaml.safe_load(file)
        return yaml_content
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file {yaml_file}: {e}")
