from yt_quick_insights import QuickInsights, YoutubeTranscript
from yt_quick_insights.config import settings
from yt_quick_insights.task import TaskDetails, tasks


def get_quick_insights(
    url: str,
    task_details: TaskDetails,
    background_information: str,
    video_language: str,
) -> QuickInsights:
    """
    Get QuickInsights object.

    Args:
        url: YouTube video url, e.g. "https://www.youtube.com/watch?v=VIDEO_ID"
        task_details: How to summarize or extract knowledge from th YouTube transcript.
        background_information: Additional contextual information about the video.
        video_language: The language of the video. If None, will try: en, de, es, fr

    Returns:
        QuickInsights object
    """
    if video_language is None:
        video_language = settings.DEFAULT_LANGUAGES

    # Get title and transcript
    yt_title, yt_transcript = YoutubeTranscript().download_from_url(
        video_url=url, video_language=video_language
    )
    # Get task
    task = tasks.get(task_details.value)
    # Extract knowledge
    return QuickInsights(
        title=yt_title,
        transcript=yt_transcript,
        task=task,
        background_information=background_information,
    )
