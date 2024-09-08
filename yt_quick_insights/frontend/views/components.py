import streamlit as st

from yt_quick_insights.config import settings
from yt_quick_insights.frontend import st_helper
from yt_quick_insights.task import TaskDetails


def user_input_form():

    with st.form("user_input_form"):

        video_url = st.text_input("YouTube Video URL")

        col1, col2 = st.columns(2)

        task = col1.selectbox(
            "Extraction Method",
            TaskDetails,
            format_func=lambda x: x.value,
            index=st_helper.default_index,
        )
        api_key = col2.text_input("OpenAI API Key")
        model_name = col1.text_input("OpenAI Model", settings.OPENAI_MODEL_NAME)
        background_information = col2.text_input("Video Background Information")

        submit = st.form_submit_button("Get Insights")

    return video_url, task, api_key, model_name, background_information, submit


def display_tokens_warning(transcript_tokens):
    if transcript_tokens > 50_000:
        st.warning(
            f"Estimated tokens in YouTube Transcript: {transcript_tokens}",
            icon=":material/warning:",
        )
    elif transcript_tokens > 20_000:
        st.info(
            f"Estimated tokens in YouTube Transcript: {transcript_tokens}",
            icon=":material/info:",
        )


def display_openai_errors(error_message, model_name):
    if "Invalid API key" in str(error_message):
        st.error(
            "Incorrect API key provided!\n"
            "You can find your API key at: https://platform.openai.com/account/api-keys.\n"
            "Please update the value in your .env file."
        )
    elif "Invalid model name" in str(error_message):
        st.error(
            f'The model "{model_name}" does not exist or you do not have access to it.\n'
            f"You can find all available models at: https://platform.openai.com/docs/models.\n"
            f"Please update the value in your .env file."
        )
