from yt_quick_insights import QuickInsights, YoutubeTranscript
from yt_quick_insights.task import ExtractionMethods, available_extraction_methods


def get_quick_insights(
    url: str,
    task_details: ExtractionMethods,
    video_language: str | list[str],
) -> QuickInsights:
    """
    Retrieve YouTube transcript and title to initialize QuickInsights object

    Args:
        url: YouTube video url, e.g. "https://www.youtube.com/watch?v=VIDEO_ID"
        task_details: How to summarize or extract knowledge from th YouTube transcript.
        video_language: The language of the video.

    Returns:
        QuickInsights object
    """
    # Get title and transcript
    yt_title, yt_transcript = YoutubeTranscript().download_from_url(
        video_url=url, video_language=video_language
    )
    # Get extraction method
    extraction_methods = available_extraction_methods.get(task_details.value)
    # Initialize QuickInsights object
    return QuickInsights(
        title=yt_title,
        transcript=yt_transcript,
        task=extraction_methods,
    )
