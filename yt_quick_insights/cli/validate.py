from typing import Optional

import typer

from yt_quick_insights.config import settings


def api_key(value: Optional[str]):
    """
    Check if the OpenAI API key is set in the .env file, in case the user has not provided a value in the CLI

    Args:
        value: Value of the parameter api-key provided in the CLI. None if not provided

    Returns
        Value of the parameter api-key provided in the CLI

    Raises:
        typer.BadParameter: If the OpenAI API key is not set in the .env file
        and the user has not provided a value in the CLI
    """
    if value is None:
        if settings.OPENAI_API_KEY is None:
            raise typer.BadParameter(get_missing_parameter_message("OpenAI API key"))
        return settings.OPENAI_API_KEY
    return value


def get_missing_parameter_message(parameter_name: str) -> str:
    """
    Return a message explaining that the parameter is required when it is not set in the .env file

    Args:
        parameter_name: Name of the CLI parameter

    Returns:
        Message explaining that the parameter is required when it is not set in the .env file
    """
    return (
        f"{parameter_name} is required when it is not set in the .env file. \n\n"
        "Recommended: Set the value in the .env file. For more information run 'ltf env-location'.\n"
        "Or set the value in the CLI"
    )
