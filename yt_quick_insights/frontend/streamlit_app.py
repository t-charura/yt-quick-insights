import streamlit as st

from yt_quick_insights.config import settings
from yt_quick_insights.frontend import components

# Page Setup
video_insights = st.Page(
    page="views/video_insights.py",
    title="From Video",
    icon=":material/youtube_activity:",
    default=True,
)

playlist_insights = st.Page(
    page="views/playlist_insights.py",
    title="From Playlist",
    icon=":material/playlist_play:",
)

extraction_methods = st.Page(
    page="views/extraction_methods.py",
    title="Extraction Methods",
    icon=":material/search_insights:",
)

custom_extraction_method = st.Page(
    page="views/yaml_file.py",
    title="Custom Extraction Method",
    icon=":material/settings:",
)

default_values_with_env = st.Page(
    page="views/env_file.py",
    title="Default Values with `.env` File",
    icon=":material/text_snippet:",
)

# Page Configuration
st.set_page_config(
    layout="wide",
    menu_items={"About": "https://github.com/t-charura/yt-quick-insights"},
)

# Load CSS before running the app
components.load_css(settings.STYLES_CSS)

# Navigation
pg = st.navigation(
    {
        "Extract Insights": [video_insights, playlist_insights],
        "Help": [extraction_methods],
        "Configuration": [custom_extraction_method, default_values_with_env],
    }
)

st.logo(str(settings.PROJECT_DIR / ".." / "docs" / "images" / "logo.png"))

st.sidebar.markdown(
    ":material/build_circle: Created by [Tendai](https://github.com/t-charura)"
)


if __name__ == "__main__":
    pg.run()
