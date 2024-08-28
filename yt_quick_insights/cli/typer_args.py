import typer

from yt_quick_insights.task import TaskDetails
from yt_quick_insights.config import settings
from yt_quick_insights.cli import validate


# Shared arguments and options

url_argument = typer.Argument(
    help='YouTube video url, e.g. "https://www.youtube.com/watch?v=VIDEO_ID"'
)

task_details_option = typer.Option(
    TaskDetails.default.value,
    "--task-details",
    "-t",
    help="How to summarize or extract knowledge from th YouTube transcript.",
)

background_information_option = typer.Option(
    "No additional information provided",
    "--background-information",
    "-b",
    help="Additional contextual information about the video.",
)

video_language_option = typer.Option(
    None,
    "--video-language",
    "-l",
    help="The language of the video. If None, will try: en, de, es, fr",
)


# Arguments and Options for extract command

model_name_option = typer.Option(
    None,
    "--model",
    "-m",
    help=(
        f"OpenAI model name. If None, takes value from .env file. "
        f"Defaults to {settings.OPENAI_MODEL_NAME} if .env file does not exist"
    ),
)

api_key_option = typer.Option(
    None,
    "--api-key",
    "-k",
    callback=validate.api_key,
    help="OpenAI API key. If None, takes value from .env file, located in: ~/.insights/.env",
)

save_output_option = typer.Option(
    False,
    "--save-output",
    "-s",
    help="Save the output as a markdown file in the current directory.",
    show_default=True,
)
