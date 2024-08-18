import re
from typing import Tuple

from langchain_community.document_loaders import YoutubeLoader


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
            loader = YoutubeLoader.from_youtube_url(
                youtube_url=video_url,
                language=video_language,
                add_video_info=True,
            )
            yt_document = loader.load()[0]
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
