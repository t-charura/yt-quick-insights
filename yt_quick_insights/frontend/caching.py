import streamlit as st

from yt_quick_insights import (
    get_quick_insights,
    PlaylistInsights,
    DeepDive,
    YoutubeTranscript,
)
from yt_quick_insights.config import settings
from yt_quick_insights.task import ExtractionMethods


@st.cache_data
def extract_insights(
    video_url: str,
    task: ExtractionMethods,
    model_name: str,
    api_key: str,
) -> str:
    """
    Extract insights from YouTube transcript

    Args:
        video_url: YouTube video url, e.g. "https://www.youtube.com/watch?v=VIDEO_ID"
        task: Specification on how to summarize the transcript.
        model_name: OpenAI model name
        api_key: OpenAI API key

    Returns:
        The summary of the transcript
    """
    quick_insights = get_quick_insights(
        url=video_url,
        task_details=task,
        video_language=settings.DEFAULT_LANGUAGES,
    )
    return quick_insights.extract(
        model_name=model_name,
        api_key=api_key,
    )


@st.cache_data(show_spinner=False)
def extract_playlist_insights(
    playlist_url: str,
    additional_instructions: str,
    extraction_method: ExtractionMethods,
    model_name: str,
    api_key: str,
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


@st.cache_data
def answer_question(
    video_url: str,
    question: str,
    model_name: str,
    api_key: str,
) -> str:
    """
    Answer a user question about a YouTube video transcript.

    Args:
        video_url: YouTube video url, e.g. "https://www.youtube.com/watch?v=VIDEO_ID"
        question: User question
        model_name: OpenAI model name
        api_key: OpenAI API key

    Returns:
        Answer to the user question
    """
    # Get title and transcript
    yt_title, yt_transcript = YoutubeTranscript().download_from_url(
        video_url=video_url, video_language=settings.DEFAULT_LANGUAGES
    )
    # Initialize DeepDive object and extract answer
    deep_dive = DeepDive(
        title=yt_title,
        transcript=yt_transcript,
        user_question=question,
    )
    return deep_dive.extract(model_name=model_name, api_key=api_key)
