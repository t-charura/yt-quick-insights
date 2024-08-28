import typer
from rich import print

from yt_quick_insights import QuickInsights, YoutubeTranscript
from yt_quick_insights import utils
from yt_quick_insights.cli import typer_args
from yt_quick_insights.config import ENV_DIR
from yt_quick_insights.config import settings
from yt_quick_insights.task import TaskDetails, tasks

app = typer.Typer(name="yt-quick-insights")


def get_quick_insights(
    url: str,
    task_details: TaskDetails,
    background_information: str,
    video_language: str,
) -> QuickInsights:
    """
    Get QuickInsights object.

    Args:
        url: YouTube video url, e.g. "https://www.youtube.com/watch?v=VIDEO_ID"
        task_details: How to summarize or extract knowledge from th YouTube transcript.
        background_information: Additional contextual information about the video.
        video_language: The language of the video. If None, will try: en, de, es, fr

    Returns:
        QuickInsights object
    """
    if video_language is None:
        video_language = settings.DEFAULT_LANGUAGES

    # Get title and transcript
    yt_title, yt_transcript = YoutubeTranscript().download_from_url(
        video_url=url, video_language=video_language
    )
    # Get task
    task = tasks.get(task_details.value)
    # Extract knowledge
    return QuickInsights(
        title=yt_title,
        transcript=yt_transcript,
        task=task,
        background_information=background_information,
    )


@app.command(name="prompt", help="Download the final prompt including the transcript.")
def download_prompt(
    url: str = typer_args.url_argument,
    task_details: TaskDetails = typer_args.task_details_option,
    background_information: str = typer_args.background_information_option,
    video_language: str = typer_args.video_language_option,
):
    quick_insights = get_quick_insights(
        url=url,
        task_details=task_details,
        background_information=background_information,
        video_language=video_language,
    )
    # Download prompt
    quick_insights.download_prompt()


@app.command(name="extract", help="Extract knowledge from the YouTube transcript.")
def extract(
    url: str = typer_args.url_argument,
    task_details: TaskDetails = typer_args.task_details_option,
    model_name: str = typer_args.model_name_option,
    api_key: str = typer_args.api_key_option,
    background_information: str = typer_args.background_information_option,
    save_output: bool = typer_args.save_output_option,
    video_language: str = typer_args.video_language_option,
):
    quick_insights = get_quick_insights(
        url=url,
        task_details=task_details,
        background_information=background_information,
        video_language=video_language,
    )
    # Use LLM to extract knowledge
    quick_insights.run(model_name=model_name, api_key=api_key, save=save_output)


@app.command(name="available-tasks", help="List all available tasks in task_details.")
def available_tasks():
    for key, task in tasks.items():
        print(f"[green bold]{key}[/green bold]:\n" f"{task}")


@app.command(name="yaml-location", help="Show where the yaml file is located.")
def yaml_location():
    print(utils.get_yaml_location())


@app.command(name="env-location", help="Show location of your .env file")
def env_location():
    print(utils.env_information(ENV_DIR / ".env"))
