import streamlit as st
from langchain_community.callbacks import OpenAICallbackHandler

from yt_quick_insights.config import settings
from yt_quick_insights.task import ExtractionMethods

# Constants
default_task = ExtractionMethods.general_summary
default_index = list(ExtractionMethods).index(default_task)

# Usage Guide Information
video_url_info = "**YouTube Video URL**: Paste the YouTube video URL in the designated field (required)."
extraction_method_info = (
    "**Extraction Method**: Select an appropriate method based on the video content. When in doubt, "
    "use the `General Summary` method. "
    "For detailed information on available methods, click [here](/extraction_methods)."
)
model_info = (
    "**OpenAI Model**: Choose your preferred model (default: `gpt-4.1-mini`). "
    "View all available models [here](https://platform.openai.com/docs/models)."
)
hideo_openai_info = (
    "**Hide Cost & Token Usage**: Check this box to hide the information about cost "
    "and token usage per insight."
)


# Functions


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

        submit = col1.form_submit_button("Get Insights")
        hide_openai_info = col2.toggle("Hide Cost & Token Usage", value=False)

        return (
            url,
            additional_instructions,
            extraction_method,
            api_key,
            model_name,
            submit,
            hide_openai_info,
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


def show_cost_and_token_usage(cb: OpenAICallbackHandler):
    col1, col2 = st.columns(2)

    dollar_cost = f"${cb.total_cost:.4f}"
    cent_cost = f"{cb.total_cost * 100:.2f}¢"

    col1.info(
        f"""
        :material/insert_text: Token Usage ({cb.successful_requests} request):
        - Input Tokens: **{cb.prompt_tokens}**
        - Output Tokens: **{cb.completion_tokens}**
        """
    )
    col2.warning(
        f"""
        :material/credit_card: Cost for this summary:
        - **{dollar_cost}**
        - **{cent_cost}**
        """
    )


def download_summary_btn(summary: str, unique_key: str):
    col1, col2 = st.columns(2)

    file_format = col2.radio("File format", (".txt", ".md"), key=f"radio_{unique_key}")

    col1.download_button(
        label="DOWNLOAD",
        data=summary,
        file_name=f"youtube_insights.{file_format}",
        mime="text/plain",
        key=f"btn_{unique_key}",
    )


def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
