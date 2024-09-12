from typing import Tuple

import streamlit as st

from yt_quick_insights import get_quick_insights, PlaylistInsights
from yt_quick_insights.config import settings
from yt_quick_insights.task import ExtractionMethods


@st.cache_data
def extract_insights(
    video_url: str,
    task: ExtractionMethods,
    model_name: str | None,
    api_key: str | None,
) -> Tuple[str, int]:
    """
    Extract insights from YouTube transcript. Returns the summary and number of tokens.

    Args:
        video_url: YouTube video url, e.g. "https://www.youtube.com/watch?v=VIDEO_ID"
        task: Specification on how to summarize the transcript.
        model_name: OpenAI model name
        api_key: OpenAI API key

    Returns:
        The summary of the transcript and the number of tokens
    """
    quick_insights = get_quick_insights(
        url=video_url,
        task_details=task,
        video_language=settings.DEFAULT_LANGUAGES,
    )

    return (
        quick_insights.extract(
            model_name=model_name,
            api_key=api_key,
        ),
        quick_insights.est_transcript_tokens,
    )


@st.cache_data(show_spinner=False)
def extract_playlist_insights(
    playlist_url: str,
    additional_instructions: str,
    extraction_method: ExtractionMethods,
    model_name: str | None,
    api_key: str | None,
) -> str:
    """
    Extract insights from YouTube playlist by summarizing all summaries
    from individual videos in the playlist.

    Args:
        playlist_url: YouTube playlist url, e.g. "https://www.youtube.com/playlist?list=PLAYLIST_ID"
        additional_instructions: Additional instructions for the summary.
        extraction_method: Specification on how to summarize the transcript.
        model_name: OpenAI model name
        api_key: OpenAI API key

    Returns:
        Condensed insights from all videos in the playlist
    """
    playlist_insights = PlaylistInsights(
        playlist_url=playlist_url,
        model_name=model_name,
        api_key=api_key,
        extraction_method=extraction_method,
    )
    return playlist_insights.extract(
        additional_instructions=additional_instructions,
    )
