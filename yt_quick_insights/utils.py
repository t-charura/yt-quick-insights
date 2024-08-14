import re
from pathlib import Path

import yaml

PROJECT_DIR = Path(__file__).resolve().parent
HOME_DIR = Path.home()


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


def load_yaml_file(file_name: str, user_yaml: bool = False) -> dict:
    """
    Load a YAML file.

    Args:
        file_name: The name of the YAML file
        user_yaml: Whether to load the YAML file from the user's home directory

    Returns:
        The content of the YAML file as a dictionary
    """
    yaml_directory = HOME_DIR / ".insights" if user_yaml else PROJECT_DIR / "data"
    yaml_file = yaml_directory / file_name

    with open(yaml_file, "r") as f:
        yaml_content = yaml.safe_load(f)

    return yaml_content


def combine_default_and_user_task_details(file_name: str = "task_details.yml") -> dict:
    """
    Combine default task details with user task details, both configured in YAML files.
    In case of duplicates, user task details will overwrite default task details.

    Args:
        file_name: The name of the YAML file, default is "task_details.yml"

    Returns:
        The combined task details as a dictionary
    """
    default_task_details = load_yaml_file(file_name)
    try:
        user_task_details = load_yaml_file(file_name, user_yaml=True)
        combined_dicts = {**default_task_details, **user_task_details}
    except FileNotFoundError:
        combined_dicts = default_task_details

    return dict(sorted(combined_dicts.items()))


tasks = combine_default_and_user_task_details()
