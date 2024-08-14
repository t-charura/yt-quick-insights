from pathlib import Path

from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import PromptTemplate
from rich import print

from yt_quick_insights import YoutubeTranscript
from yt_quick_insights import utils
from yt_quick_insights.task import tasks


class Prompt:
    """
    This class provides functionality to create and save a prompt to a text file.
    The prompt includes the title, task, background information, and video transcript.
    """

    def __init__(
        self,
        video_url: str,
        task: str,
        background_information: str,
        video_language: str | list[str],
    ):
        """
        Initialize the class with the video URL, task, background information, and video language.

        Args:
            video_url: The URL of the YouTube video. Example: "https://www.youtube.com/watch?v=VIDEO_ID"
            task: Specification on how to summarize the transcript.
            background_information: Additional contextual information about the video.
            video_language: The language of the transcript. Example: "en" or ["en", "de"]
        """
        self.title, self.transcript = YoutubeTranscript().download_from_url(
            video_url=video_url, video_language=video_language
        )
        self.task = tasks.get(task)
        self.template = utils.load_yaml_file("prompt.yml").get("prompt")
        self.background_information = background_information

    def create(self) -> PromptValue:
        """
        Create the prompt with the title, task, background information, and video transcript.

        Returns:
            PromptValue: Final PromptTemplate containing all variables.
        """
        prompt_template = PromptTemplate(
            template=self.template,
            input_variables=[
                "video_title",
                "task",
                "background_information",
                "youtube_transcript",
            ],
        )
        return prompt_template.invoke(
            {
                "video_title": self.title,
                "task": self.task.rstrip(),
                "background_information": self.background_information,
                "youtube_transcript": self.transcript,
            }
        )

    def save_to_file(self) -> None:
        """
        Save the final prompt to a text file in your current working directory.
        """
        file_name = f"{utils.clean_youtube_title(self.title)}.txt"
        prompt = self.create()
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(prompt.text)

        print(f'File saved at: "{Path.cwd() / file_name}"')
