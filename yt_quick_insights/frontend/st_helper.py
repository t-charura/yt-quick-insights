from typing import Tuple

import streamlit as st

from yt_quick_insights.cli import helper
from yt_quick_insights.config import settings
from yt_quick_insights.task import TaskDetails

default_task = TaskDetails.default
default_index = list(TaskDetails).index(default_task)


@st.cache_data
def extract_insights(
    video_url, task, model_name, api_key, background_information
) -> Tuple[str, int]:
    """
    Extract insights from YouTube transcript. Returns the summary and number of tokens.

    Args:
        video_url: YouTube video url, e.g. "https://www.youtube.com/watch?v=VIDEO_ID"
        task: Specification on how to summarize the transcript.
        model_name: OpenAI model name
        api_key: OpenAI API key
        background_information: Additional contextual information about the video.

    Returns:
        The summary of the transcript and the number of tokens
    """
    quick_insights = helper.get_quick_insights(
        url=video_url,
        task_details=task,
        background_information=background_information,
        video_language=settings.DEFAULT_LANGUAGES,
    )

    return (
        quick_insights.extract(
            model_name=model_name if model_name else settings.OPENAI_MODEL_NAME,
            api_key=api_key if api_key else settings.OPENAI_API_KEY,
        ),
        quick_insights.est_transcript_tokens,
    )
