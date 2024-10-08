import re
from pathlib import Path

import yaml

from yt_quick_insights.config import settings


def clean_youtube_video_title(video_title: str) -> str:
    """
    Remove unwanted characters from the YouTube video title, because the title is used as a filename.

    Args:
        video_title: The title of the YouTube video

    Returns:
        The cleaned video title
    """
    allowed_chars = re.sub(r"[^a-z0-9 ]", "", video_title.lower()).strip()
    return re.sub(r"\s+", " ", allowed_chars).replace(" ", "_")[0:200]


def load_yaml_file(file_name: str, directory: Path) -> dict[str, str]:
    """
    Load a YAML file from either the project directory or the user's home directory

    Args:
        file_name: The name of the YAML file
        directory: The directory where the YAML file is located

    Returns:
        The content of the YAML file as a dictionary

    Raises:
        yaml.YAMLError: If there is an error parsing the YAML file
    """
    yaml_file = directory / file_name

    try:
        with open(yaml_file, "r") as file:
            yaml_content = yaml.safe_load(file)
        return yaml_content
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file {yaml_file}: {e}")


def get_yaml_location() -> str:
    """
    Get the location of the yaml file where the user can define their task details.

    Returns:
        The location of the yaml file
    """
    return (
        "YouTube Quick Insights is looking for the yaml file at the following location:\n"
        f'--> [green bold]{settings.HOME_DIR / ".insights" / "task_details.yaml"}[/green bold] <--\n\n'
        f"Check https://github.com/t-charura/yt-quick-insights for an example yaml file."
    )
