import streamlit as st

from yt_quick_insights.config import settings
from yt_quick_insights.task import ExtractionMethods

default_task = ExtractionMethods.default
default_index = list(ExtractionMethods).index(default_task)


def format_dropdown_label(item):
    string = item.value
    return string.replace("_", " ").title()


def user_input_form(playlist: bool = False):

    with st.form("user_input_form"):

        url_label = "Playlist URL" if playlist else "YouTube Video URL"
        url = st.text_input(url_label)

        if playlist:
            playlist_topic = st.text_input("Playlist Topic & Focus")
        else:
            playlist_topic = ""

        col1, col2 = st.columns(2)

        if playlist:
            task = ExtractionMethods.default
            background_information = ""

        else:
            task = col1.selectbox(
                "Extraction Method",
                ExtractionMethods,
                format_func=format_dropdown_label,
                index=default_index,
            )
            background_information = col2.text_input("Video Background Information")

        api_key = col2.text_input("OpenAI API Key")
        model_name = col1.text_input("OpenAI Model", settings.OPENAI_MODEL_NAME)

        submit = st.form_submit_button("Get Insights")

        return (
            url,
            playlist_topic,
            task,
            api_key,
            model_name,
            background_information,
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
