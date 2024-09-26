import streamlit as st
import typer
from langchain_community.callbacks import get_openai_callback

from yt_quick_insights.config import settings
from yt_quick_insights.frontend import caching
from yt_quick_insights.frontend.views import components
from yt_quick_insights.frontend.views import deep_dive as dd


# Set session states
def initialize_session_state():
    """Initialize session states variables."""
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "submitted_deep_dive" not in st.session_state:
        st.session_state.submitted_deep_dive = False
    if "video_insights" not in st.session_state:
        st.session_state.video_insights = ""
    if "deep_dive" not in st.session_state:
        st.session_state.deep_dive = ""
    if "url" not in st.session_state:
        st.session_state.url = ""


def display_title_and_description():
    st.title(":material/youtube_activity: YouTube Quick Insights")
    st.markdown(
        "##### Extract valuable insights from YouTube Videos without watching them"
    )


def display_usage_guide():
    with st.expander(":material/help:  Usage Guide: Video Insights"):
        st.markdown(
            f"""
            1. {components.video_url_info} 
            2. {components.extraction_method_info}
            3. {components.model_info}
            4. **OpenAI API Key**: Provide your API key in one of the following ways:
               - Enter it directly in the provided field.
               - Set it in the `.env` file (recommended). Learn more [here](/env_file).
               - Store the key in an environment variable called: `OPENAI_API_KEY`.
            5. {components.hideo_openai_info}
            """,
            unsafe_allow_html=True,
        )


def process_user_inputs():
    # Get Input Form
    video_url, _, extraction_method, api_key, model_name, submit, hide_openai_info = (
        components.user_input_form()
    )

    # Extract insights and set session states
    if submit:
        # Check if API key and model name are provided
        if not api_key:
            api_key = settings.OPENAI_API_KEY
        if not model_name:
            model_name = settings.OPENAI_MODEL_NAME

        try:
            with get_openai_callback() as cb:
                st.session_state.video_insights = caching.extract_insights(
                    video_url=video_url,
                    task=extraction_method,
                    model_name=model_name,
                    api_key=api_key,
                )
            if not hide_openai_info:
                components.show_cost_and_token_usage(cb)
            st.session_state.url = video_url
            st.session_state.submitted = True
        except ValueError:
            st.error(
                "Please provide a valid YouTube URL in the form of 'https://www.youtube.com/watch?v=VIDEO_ID'"
            )
            st.session_state.submitted = False
            st.session_state.url = None
        except typer.Abort as e:
            components.display_openai_errors(e, model_name)
            st.session_state.submitted = False
            st.session_state.url = None


# Display insights
def display_results():
    if st.session_state.submitted:
        result_container = st.container(border=True)
        result_container.markdown(st.session_state.video_insights)

        if st.session_state.video_insights:
            col1, col2 = st.columns(2)

            file_format = col2.radio("File format", (".txt", ".md"))

            col1.download_button(
                label="DOWNLOAD",
                data=st.session_state.video_insights,
                file_name=f"youtube_insights.{file_format}",
                mime="text/plain",
            )


def render_video_insights():
    """Create homepage structure."""

    initialize_session_state()
    display_title_and_description()
    video_insights_tab, deep_dive_tab = st.tabs(["Video Insights", "Deep Dive"])

    with video_insights_tab:
        display_usage_guide()
        process_user_inputs()
        display_results()

    with deep_dive_tab:
        dd.render_deep_dive()


render_video_insights()
