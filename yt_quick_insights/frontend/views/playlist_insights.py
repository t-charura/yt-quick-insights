from urllib.error import HTTPError

import streamlit as st
import typer

from yt_quick_insights.config import settings
from yt_quick_insights.frontend import caching
from yt_quick_insights.frontend import components


def initialize_session_state():
    """Initialize session states variables."""
    if "submitted_playlist" not in st.session_state:
        st.session_state.submitted_playlist = False
    if "playlist_insights" not in st.session_state:
        st.session_state.playlist_insights = ""


def display_title_and_description():
    st.title(":material/playlist_play: Playlist Quick Insights")
    st.markdown(
        "##### Extract valuable insights from YouTube Playlists without watching them"
    )


def display_help():
    with st.expander(":material/help:  Usage Guide"):
        st.markdown(
            """
            1. **Playlist URL**: Paste the YouTube playlist URL in the designated field (required).
            2. **Additional Instructions**: Additional instructions for summarizing the playlist (optional).
                - Example: Playlist with 10 videos about "Productivity"
                - Additional Instructions: "What is the best way to do Goal Setting?"
            3. **Extraction Method**: Select an appropriate method based on the video content. When in doubt, 
               use the `General Summary` method. 
               For detailed information on available methods, click [here](/extraction_methods).
            4. **OpenAI Model**: Choose your preferred model (default: `gpt-4o-mini`).
               View all available models [here](https://platform.openai.com/docs/models).
            5. **OpenAI API Key**: Provide your API key in one of the following ways:
               - Enter it directly in the provided field.
               - Set it in the `.env` file (recommended). Learn more [here](/env_file).
               - Store the key in an environment variable called: `OPENAI_API_KEY`.
            """,
            unsafe_allow_html=True,
        )


def process_user_inputs():
    # Get Input Form
    (
        playlist_url,
        additional_instructions,
        extraction_method,
        api_key,
        model_name,
        submit,
    ) = components.user_input_form(playlist=True)

    # Extract insights and set session states
    if submit:
        # Check if API key and model name are provided
        if not api_key:
            api_key = settings.OPENAI_API_KEY
        if not model_name:
            model_name = settings.OPENAI_MODEL_NAME

        if not additional_instructions:
            additional_instructions = (
                "No additional instructions, focus on the instructions above"
            )

        try:
            st.session_state.playlist_insights = caching.extract_playlist_insights(
                playlist_url=playlist_url,
                additional_instructions=additional_instructions,
                extraction_method=extraction_method,
                model_name=model_name,
                api_key=api_key,
            )
            st.session_state.submitted_playlist = True
        except (HTTPError, KeyError):
            st.error(
                "Please provide a valid YouTube Playlist URL in the form of 'https://www.youtube.com/playlist?list=PLAYLIST_ID'"
            )
            st.session_state.submitted_playlist = False
        except typer.Abort as e:
            components.display_openai_errors(e, model_name)
            st.session_state.submitted_playlist = False


def display_results():
    if st.session_state.submitted_playlist:
        result_container = st.container(border=True)
        result_container.markdown(st.session_state.playlist_insights)

        if st.session_state.playlist_insights:
            col1, col2 = st.columns(2)

            file_format = col2.radio("File format", (".txt", ".md"))

            col1.download_button(
                label="DOWNLOAD",
                data=st.session_state.playlist_insights,
                file_name=f"youtube_insights.{file_format}",
                mime="text/plain",
            )


def render_playlist_insights():
    """Create playlist insights structure."""
    initialize_session_state()
    display_title_and_description()
    display_help()
    process_user_inputs()
    display_results()


render_playlist_insights()
