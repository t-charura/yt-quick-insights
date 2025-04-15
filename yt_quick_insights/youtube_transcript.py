import re
from typing import Tuple
from urllib.error import HTTPError

from langchain_community.document_loaders import YoutubeLoader
from langchain_core.documents import Document
from pytube.exceptions import PytubeError


class YoutubeTranscript:
    """
    This class provides functionality to retrieve the transcript and title
    of a YouTube video given its URL, and clean the text for further processing.
    """

    def download_from_url(
        self, video_url: str, video_language: str | list[str]
    ) -> Tuple[str, str]:
        """
        Download the transcript and title of a YouTube video, based on the URL.

        Args:
            video_url: The URL of the YouTube video. Example: "https://www.youtube.com/watch?v=VIDEO_ID"
            video_language: The language of the transcript. Example: "en" or ["en", "de"]

        Returns:
            The title and transcript of the YouTube video.

        Raises:
            ValueError: If the URL is not valid.
            IndexError: If the video does not have a transcript.
        """
        try:
            # Try loading the transcript from the YouTube URL - not all videos have transcripts
            yt_document = self._load(
                video_url=video_url,
                video_language=video_language,
                add_video_info=True,
            )
        except (PytubeError, HTTPError) as e:
            # Common error, when YouTube makes changes to their API structure and "pytube" has not yet adjusted
            # pytube is used by langchain's YoutubeLoader to fetch video details
            yt_document = self._load(
                video_url=video_url,
                video_language=video_language,
                add_video_info=False,
            )
            return (
                "YouTube Video Title could not be retrieved",
                self._clean_text(yt_document.page_content),
            )
        except ValueError:
            raise ValueError(
                "Please provide a valid YouTube URL "
                'in the form of "https://www.youtube.com/watch?v=VIDEO_ID".'
            )
        except IndexError:
            raise IndexError(
                "Video does not have a transcript. Please try another video."
            )

        return (
            self._clean_text(yt_document.metadata.get("title")),
            self._clean_text(yt_document.page_content),
        )

    @staticmethod
    def _load(
        video_url: str, video_language: str | list[str], add_video_info: bool
    ) -> Document:
        """
        Load the transcript from the YouTube URL with the option to add video info.

        Args:
            video_url: The URL of the YouTube video. Example: "https://www.youtube.com/watch?v=VIDEO_ID"
            video_language: The language of the transcript. Example: "en" or ["en", "de"]
            add_video_info: Whether to add video info to the transcript. Example: True or False

        Returns:
            A Document object containing the transcript of the YouTube video and metadata.

        """
        loader = YoutubeLoader.from_youtube_url(
            youtube_url=video_url,
            language=video_language,
            add_video_info=add_video_info,
        )
        return loader.load()[0]

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Clean the text of unwanted characters and whitespaces.

        Args:
            text: The text to clean.

        Returns:
            The cleaned text.
        """
        # Remove unwanted characters
        cleaned = re.sub(r"(\xa0|\n|\[Music])", " ", text)
        # Replace multiple whitespaces with single whitespace
        return re.sub(r"\s+", " ", cleaned)
