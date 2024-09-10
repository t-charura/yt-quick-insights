import streamlit as st
from langchain_core.prompts import PromptTemplate
from pytube import Playlist

from yt_quick_insights import get_quick_insights
from yt_quick_insights import utils
from yt_quick_insights.config import settings
from yt_quick_insights.task import TaskDetails


class PlaylistInsights:
    """
    This class provides functionality to extract insights from the content of a YouTube playlist.
    It collects video URLs from the playlist and extracts insights from each video,
    and consolidates them into a single cohesive summary using a language model.
    """

    def __init__(self, playlist_url: str, model_name: str, api_key: str):
        """
        Initialize the class with the YouTube playlist URL, OpenAI model name, and OpenAI API key.

        Args:
            playlist_url: YouTube playlist URL
            model_name: OpenAI model name
            api_key: OpenAI API key
        """
        self.yt_video_urls = Playlist(playlist_url).video_urls
        self.model_name = model_name
        self.api_key = api_key
        self.summary_collection: list[str] = list()
        self.prompt_template = self._load_prompt_template()
        # Final prompt template

    @staticmethod
    def _load_prompt_template() -> PromptTemplate:
        """Load template from YAML file and convert into PromptTemplate"""
        template = utils.load_yaml_file(
            file_name="playlist_prompt.yml", directory=settings.PROJECT_DIR / "data"
        )

        return PromptTemplate(
            template=template.get("playlist_prompt"),
            input_variables=[
                "topic_and_focus",
                "summaries",
            ],
        )

    def _collect_summaries(self):
        """
        Collect summary from each video in the playlist and store it in the summary_collection list.
        """
        progress_bar = st.progress(0, text="Downloading Videos")
        num_videos = len(self.yt_video_urls)
        for idx, url in enumerate(self.yt_video_urls, start=1):  # type: str
            progress_bar.progress(
                idx * int(100 / num_videos),
                text=f"Extracting Insights from Video {idx} of {num_videos}",
            )
            summary = get_quick_insights(
                url=url,
                task_details=TaskDetails.default,
                background_information="",
                video_language=settings.DEFAULT_LANGUAGES,
            ).extract(model_name=self.model_name, api_key=self.api_key)

            self.summary_collection.append(summary)

        progress_bar.empty()

    def extract(self, topic_and_focus: str) -> str:
        """
        Extract insights from all videos in the playlist
        and consolidate them into a single cohesive summary.

        Args:
            topic_and_focus: The topic and focus of the playlist

        Returns:
            Consolidated insights from all videos in the playlist
        """
        self._collect_summaries()

        with st.spinner("Consolidate insights from all videos ..."):
            joined_summaries = "\n\n\n --- Next Summary --- \n\n\n".join(
                self.summary_collection
            )

            llm = utils.initialize_llm(model_name=self.model_name, api_key=self.api_key)
            chain = self.prompt_template | llm
            return chain.invoke(
                {
                    "topic_and_focus": topic_and_focus,
                    "summaries": joined_summaries,
                }
            ).content
