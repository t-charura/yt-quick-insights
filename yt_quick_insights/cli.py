import typer
from rich import print

from yt_quick_insights import Prompt
from yt_quick_insights import utils
from yt_quick_insights.config import settings
from yt_quick_insights.task import TaskDetails, tasks

app = typer.Typer(name="yt-quick-insights")


@app.command(
    name="download", help="Download the final prompt including the transcript."
)
def download(
    url: str = typer.Argument(
        help='YouTube video url, e.g. "https://www.youtube.com/watch?v=VIDEO_ID"'
    ),
    task_details: TaskDetails = typer.Option(
        TaskDetails.default.value,
        "--task-details",
        "-t",
        help="How to summarize or extract knowledge from th YouTube transcript.",
    ),
    background_information: str = typer.Option(
        "No additional information provided",
        "--background-information",
        "-b",
        help="Additional contextual information about the video.",
    ),
    video_language: str = typer.Option(
        None,
        "--video-language",
        "-l",
        help="The language of the video. If None, will try: en, de, es, fr",
    ),
):
    if video_language is None:
        video_language = settings.DEFAULT_LANGUAGES

    Prompt(
        video_url=url,
        task=task_details.value,
        background_information=background_information,
        video_language=video_language,
    ).save_to_file()


@app.command(name="available-tasks", help="List all available tasks in task_details.")
def available_tasks():
    for key, task in tasks.items():
        print(f"[green bold]{key}[/green bold]:\n" f"{task}")


@app.command(name="yaml-location", help="Show where the yaml file is located.")
def yaml_location():
    print(utils.get_yaml_location())
