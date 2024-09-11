from urllib.error import HTTPError

import streamlit as st
import typer

from yt_quick_insights.frontend import caching
from yt_quick_insights.frontend import components


def initialize_session_state():
    """Initialize session states variables."""
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
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
            2. **Playlist Topic & Focus**: Add description later
            3. **OpenAI API Key**: Provide your API key in one of the following ways:
               - Enter it directly in the provided field.
               - Set it in the `.env` file (recommended). Learn more [here](/env_file).
               - Store the key in an environment variable called: `OPENAI_API_KEY`.
            4. **OpenAI Model**: Choose your preferred model (default: `gpt-4o-mini`).
               View all available models [here](https://platform.openai.com/docs/models).
            """,
            unsafe_allow_html=True,
        )


def process_user_inputs():
    # Get Input Form
    (
        playlist_url,
        playlist_topic,
        task,
        api_key,
        model_name,
        background_information,
        submit,
    ) = components.user_input_form(playlist=True)

    # Extract insights and set session states
    if submit:
        try:
            st.session_state.playlist_insights = caching.extract_playlist_insights(
                playlist_url=playlist_url,
                topic_and_focus=playlist_topic,
                model_name=model_name,
                api_key=api_key,
            )
        except (HTTPError, KeyError):
            st.error(
                "Please provide a valid YouTube Playlist URL in the form of 'https://www.youtube.com/playlist?list=PLAYLIST_ID'"
            )
        except typer.Abort as e:
            components.display_openai_errors(e, model_name)

        st.session_state.submitted = True


def display_results():
    if st.session_state.submitted:
        st.markdown(st.session_state.playlist_insights)

        if st.session_state.playlist_insights:
            st.divider()
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
