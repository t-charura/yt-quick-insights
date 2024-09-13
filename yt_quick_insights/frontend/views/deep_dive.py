import streamlit as st
import typer

from yt_quick_insights.config import settings
from yt_quick_insights.frontend import caching
from yt_quick_insights.frontend.views import components


def display_usage_guide():
    with st.expander(":material/help: Usage Guide"):
        st.markdown(
            """
            1. **YouTube Video URL**: Paste the YouTube video URL in the designated field (required).
            2. **Question**: Ask a question about the video.
            3. **OpenAI Model**: Choose your preferred model (default: `gpt-4o-mini`).
               View all available models [here](https://platform.openai.com/docs/models).
            4. **OpenAI API Key**: Provide your API key in one of the following ways:
               - Enter it directly in the provided field.
               - Set it in the `.env` file (recommended). Learn more [here](/env_file).
               - Store the key in an environment variable called: `OPENAI_API_KEY`.
            """,
            unsafe_allow_html=True,
        )


def user_input_form():

    with st.form("deep_dive_user_input_form"):

        video_url = st.session_state.url if st.session_state.url else None

        url = st.text_input("YouTube Video URL", value=video_url)

        query = st.text_area(
            "Question",
            placeholder="Ask your question ...",
        )
        col1, col2 = st.columns(2)

        api_key = col2.text_input("OpenAI API Key", type="password")
        model_name = col1.text_input("OpenAI Model", settings.OPENAI_MODEL_NAME)

        submit = st.form_submit_button("Get Insights")

        return (
            url,
            query,
            api_key,
            model_name,
            submit,
        )


def process_user_inputs():
    url, query, api_key, model_name, submit = user_input_form()
    if submit:
        # Check if API key and model name are provided
        if not api_key:
            api_key = settings.OPENAI_API_KEY
        if not model_name:
            model_name = settings.OPENAI_MODEL_NAME

        try:
            st.session_state.deep_dive = caching.answer_question(
                video_url=url, question=query, api_key=api_key, model_name=model_name
            )
            st.session_state.submitted_deep_dive = True
        except ValueError:
            st.error(
                "Please provide a valid YouTube URL in the form of 'https://www.youtube.com/watch?v=VIDEO_ID'"
            )
            st.session_state.submitted_deep_dive = False
        except typer.Abort as e:
            components.display_openai_errors(e, model_name)
            st.session_state.submitted_deep_dive = False


def display_results():
    if st.session_state.submitted_deep_dive:
        result_container = st.container(border=True)
        result_container.markdown(st.session_state.deep_dive)


def render_deep_dive():
    display_usage_guide()
    process_user_inputs()
    display_results()
