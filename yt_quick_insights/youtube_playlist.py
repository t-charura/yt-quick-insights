import streamlit as st
from langchain_core.prompts import PromptTemplate
from pytube import Playlist

from yt_quick_insights import get_quick_insights
from yt_quick_insights import utils
from yt_quick_insights.config import settings
from yt_quick_insights.task import ExtractionMethods


class PlaylistInsights:
    """
    This class provides functionality to extract insights from the content of a YouTube playlist.
    It collects video URLs from the playlist and extracts insights from each video,
    and consolidates them into a single cohesive summary using a language model.
    """

    def __init__(
        self,
        playlist_url: str,
        model_name: str,
        api_key: str,
        extraction_method: ExtractionMethods,
    ):
        """
        Initialize the class with the YouTube playlist URL, OpenAI model name, and OpenAI API key.

        Args:
            playlist_url: YouTube playlist URL
            model_name: OpenAI model name
            api_key: OpenAI API key
            extraction_method: Method used to extract insights from individual videos
        """
        self.playlist = Playlist(playlist_url)
        self.playlist_length = self.playlist.length
        self.model_name = model_name
        self.api_key = api_key
        self.summary_collection: list[str] = list()
        self.prompt_template = self._load_prompt_template()
        self.extraction_method = extraction_method

    @staticmethod
    def _load_prompt_template() -> PromptTemplate:
        """Load template from YAML file and convert into PromptTemplate"""
        template = utils.load_yaml_file(
            file_name="playlist_prompt.yml", directory=settings.PROJECT_DIR / "data"
        )

        return PromptTemplate(
            template=template.get("playlist_prompt"),
            input_variables=[
                "additional_instructions",
                "summaries",
            ],
        )

    def _collect_summaries(self):
        """
        Collect summary from each video in the playlist and store it in the summary_collection list.
        """
        info = st.info(f"{self.playlist_length} videos were found in the playlist.")
        progress_bar = st.progress(0, text="Downloading Videos")
        for idx, url in enumerate(self.playlist.video_urls, start=1):  # type: str
            progress_bar.progress(
                idx * int(100 / self.playlist_length),
                text=f"Extracting Insights from Video {idx} of {self.playlist_length}",
            )
            summary = get_quick_insights(
                url=url,
                task_details=self.extraction_method,
                video_language=settings.DEFAULT_LANGUAGES,
            ).extract(model_name=self.model_name, api_key=self.api_key)

            self.summary_collection.append(summary)

        info.empty()
        progress_bar.empty()

    def extract(self, additional_instructions: str) -> str:
        """
        Extract insights from all videos in the playlist
        and consolidate them into a single cohesive summary.

        Args:
            additional_instructions: Additional instructions for the summary

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
                    "additional_instructions": additional_instructions,
                    "summaries": joined_summaries,
                }
            ).content
