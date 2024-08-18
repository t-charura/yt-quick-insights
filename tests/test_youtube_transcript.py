from unittest.mock import patch, MagicMock

import pytest

from yt_quick_insights import YoutubeTranscript


@pytest.fixture
def youtube_transcript():
    return YoutubeTranscript()


@pytest.fixture
def mock_loader():
    with patch("yt_quick_insights.youtube_transcript.YoutubeLoader") as mock:
        yield mock


def test_download_from_url_success(youtube_transcript, mock_loader):
    mock_document = MagicMock()
    mock_document.metadata = {"title": "Test Title"}
    mock_document.page_content = "Test Content"
    mock_loader.from_youtube_url.return_value.load.return_value = [mock_document]

    title, transcript = youtube_transcript.download_from_url(
        "https://www.youtube.com/watch?v=VIDEO_ID", "en"
    )

    assert title == "Test Title"
    assert transcript == "Test Content"
    mock_loader.from_youtube_url.assert_called_once()


def test_download_from_url_invalid_url(youtube_transcript, mock_loader):
    mock_loader.from_youtube_url.side_effect = ValueError

    with pytest.raises(ValueError, match="Please provide a valid YouTube URL"):
        youtube_transcript.download_from_url("invalid_url", "en")


def test_download_from_url_no_transcript(youtube_transcript, mock_loader):
    mock_loader.from_youtube_url.return_value.load.side_effect = IndexError

    with pytest.raises(IndexError, match="Video does not have a transcript"):
        youtube_transcript.download_from_url(
            "https://www.youtube.com/watch?v=VIDEO_ID", "en"
        )


def test_clean_text():
    text = "Hello\xa0world\n[Music] This is a test"
    cleaned_text = YoutubeTranscript._clean_text(text)
    assert cleaned_text == "Hello world This is a test"
