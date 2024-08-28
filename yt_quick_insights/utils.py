import re
from pathlib import Path

import yaml
from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.markdown import Markdown

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


def initialize_llm(model_name: str, api_key: str) -> ChatOpenAI:
    """
    Return an LLM instance

    Returns:
        LLM instance
    """
    return ChatOpenAI(
        model_name=model_name,
        api_key=api_key,
        temperature=0,
    )


def save_to_file(file_name: str, content: str) -> None:
    """
    Save the given result to a file with the given file name.

    Args:
        file_name: The name of the file to save to.
        content: The content to save to the file.
    """
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(content)


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


def env_information(file_path: Path) -> str:
    return (
        "Language Transfer Flashcards (ltf) is looking for the .env file at the following location:\n"
        f"--> [green bold]{file_path}[/green bold] <--\n\n"
        "File must contain the following variables: 'OPENAI_API_KEY', 'OPENAI_MODEL_NAME' and 'TARGET_LANGUAGE'. \n"
        "To see all valid values for these variables, run 'ltf csv --help'\n\n"
        # TODO: update link for example .env file (add a screenshot to README)
        "Check https://github.com/t-charura/yt-quick-insights for an example .env file."
    )


def show_markdown_output(string) -> None:
    """Show markdown output in the console."""
    console = Console()
    console.print(Markdown(string))
