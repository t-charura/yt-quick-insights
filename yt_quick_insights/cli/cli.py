import subprocess

import typer
from rich import print

from yt_quick_insights import utils
from yt_quick_insights.config import settings

app = typer.Typer(name="yt-quick-insights")


@app.command(name="run", help="Start YouTube Quick Insights app.")
def run_youtube_quick_insights():
    subprocess.run(["streamlit", "run", str(settings.STREAMLIT_APP)])


@app.command(name="env-location", help="Display the location of the .env file.")
def env_location():
    print(utils.env_information())


@app.command(
    name="yaml-location", help="Display the location of the YAML configuration file."
)
def yaml_location():
    print(utils.get_yaml_location())
