import streamlit as st

from yt_quick_insights.config import settings
from yt_quick_insights.task import ExtractionMethods

default_task = ExtractionMethods.general_summary
default_index = list(ExtractionMethods).index(default_task)


def format_dropdown_label(item):
    string = item.value
    return string.replace("_", " ").title()


def user_input_form(playlist: bool = False):

    with st.form("playlist_user_input_form" if playlist else "user_input_form"):

        url_label = "Playlist URL" if playlist else "YouTube Video URL"
        url = st.text_input(url_label)

        if playlist:
            additional_instructions = st.text_area(
                "Additional Instructions (optional)",
            )
        else:
            additional_instructions = ""

        em_label = (
            "Extraction Method used for individual videos"
            if playlist
            else "Extraction Method"
        )
        extraction_method = st.selectbox(
            em_label,
            ExtractionMethods,
            format_func=format_dropdown_label,
            index=default_index,
        )

        col1, col2 = st.columns(2)

        api_key = col2.text_input("OpenAI API Key", type="password")
        model_name = col1.text_input("OpenAI Model", settings.OPENAI_MODEL_NAME)

        submit = st.form_submit_button("Get Insights")

        return (
            url,
            additional_instructions,
            extraction_method,
            api_key,
            model_name,
            submit,
        )


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
            """
            ##### Invalid API key provided!
            - Make sure your API key is valid.
            - Generate a new API key at: https://platform.openai.com/account/api-keys.
            - Check the "Usage Guide" above to learn how to set your API key correctly.
            """
        )
    elif "Invalid model name" in str(error_message):
        st.error(
            f"""
            ##### Invalid OpenAI model name provided!
            - The model "{model_name}" does not exist or you do not have access to it.
            - You can find all available models at: https://platform.openai.com/docs/models.
            - Learn how to change the default value for OpenAI Model, click [here](/env_file).
            """
        )
