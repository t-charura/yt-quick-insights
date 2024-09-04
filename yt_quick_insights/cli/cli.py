from pathlib import Path

import typer
from rich import print

from yt_quick_insights import utils
from yt_quick_insights.cli import typer_args, helper
from yt_quick_insights.config import ENV_DIR
from yt_quick_insights.task import TaskDetails, tasks

app = typer.Typer(name="yt-quick-insights")


@app.command(name="prompt", help="Download the final prompt including the transcript.")
def download_prompt(
    url: str = typer_args.url_argument,
    task_details: TaskDetails = typer_args.task_details_option,
    background_information: str = typer_args.background_information_option,
    video_language: str = typer_args.video_language_option,
):
    # Get Prompt
    quick_insights = helper.get_quick_insights(
        url=url,
        task_details=task_details,
        background_information=background_information,
        video_language=video_language,
    )
    prompt = quick_insights.get_prompt()
    # Save prompt to file
    file_name = f"{utils.clean_youtube_video_title(quick_insights.title)}.txt"
    utils.save_to_file(file_name=file_name, content=prompt)
    print(f'File saved at: "{Path.cwd() / file_name}"')


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
    # Use LLM to extract knowledge
    quick_insights = helper.get_quick_insights(
        url=url,
        task_details=task_details,
        background_information=background_information,
        video_language=video_language,
    )
    insights = quick_insights.extract(model_name=model_name, api_key=api_key)

    if save_output:
        file_name = f"{utils.clean_youtube_video_title(quick_insights.title)}.md"
        utils.save_to_file(file_name=file_name, content=insights)

    utils.show_markdown_output(insights)


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
