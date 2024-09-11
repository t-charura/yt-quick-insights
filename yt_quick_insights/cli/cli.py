import subprocess

import typer

from yt_quick_insights.config import settings

app = typer.Typer(name="yt-quick-insights")


@app.command(help="Start YouTube Quick Insights app.")
def run_youtube_quick_insights():
    subprocess.run(["streamlit", "run", str(settings.STREAMLIT_APP)])
