import streamlit as st
import typer

from yt_quick_insights.frontend import st_helper
from yt_quick_insights.frontend.views import components


# Set session states
def initialize_session_state():
    """Initialize session states variables."""
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "insights" not in st.session_state:
        st.session_state.insights = ""


def display_title_and_description():
    st.title(":material/youtube_activity: YouTube Quick Insights")
    st.markdown(
        "##### Extract valuable insights from YouTube Videos without watching them"
    )

    st.markdown(
        """
        """
    )


def display_help():
    with st.expander(":material/help:  Usage Guide"):
        st.markdown(
            """
            1. **YouTube Video URL**: Paste the YouTube video URL in the designated field (required).
            2. **Extraction Method**: Select an appropriate method based on the video content. When in doubt, use the default method. 
               For detailed information on available methods, click [here](/task_details).
            3. **OpenAI API Key**: Provide your API key in one of the following ways:
               - Enter it directly in the provided field.
               - Set it in the `.env` file (recommended). Learn more [here](/env_file).
               - Store the key in an environment variable called: `OPENAI_API_KEY`.
            4. **OpenAI Model**: Choose your preferred model (default: `gpt-4o-mini`).
               View all available models [here](https://platform.openai.com/docs/models).
            5. **Video Background Information**: (Optional) Additional contextual information about the video.
            """,
            unsafe_allow_html=True,
        )


def process_user_inputs():
    # Get Input Form
    video_url, task, api_key, model_name, background_information, submit = (
        components.user_input_form()
    )

    # Extract insights and set session states
    if submit:
        try:
            st.session_state.insights, transcript_tokens = st_helper.extract_insights(
                video_url=video_url,
                task=task,
                model_name=model_name,
                api_key=api_key,
                background_information=background_information,
            )
            components.display_tokens_warning(transcript_tokens)
        except ValueError:
            st.error(
                "Please provide a valid YouTube URL in the form of 'https://www.youtube.com/watch?v=VIDEO_ID'"
            )
        except typer.Abort as e:
            components.display_openai_errors(e, model_name)

        st.session_state.submitted = True


# Display insights
def display_results():
    if st.session_state.submitted:
        st.markdown(st.session_state.insights)

        if st.session_state.insights:
            st.divider()
            col1, col2 = st.columns(2)

            file_format = col2.radio("File format", (".txt", ".md"))

            col1.download_button(
                label="DOWNLOAD",
                data=st.session_state.insights,
                file_name=f"youtube_insights.{file_format}",
                mime="text/plain",
            )


def render_homepage():
    """Create homepage structure."""
    initialize_session_state()
    display_title_and_description()
    display_help()
    process_user_inputs()
    display_results()


render_homepage()
