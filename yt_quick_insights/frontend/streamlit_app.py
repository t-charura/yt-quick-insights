import streamlit as st

from yt_quick_insights.config import settings

# Page Setup
homepage = st.Page(
    page="views/homepage.py",
    title="YouTube Quick Insights",
    icon=":material/youtube_activity:",
    default=True,
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

task_details = st.Page(
    page="views/task_details.py",
    title="Available Extraction Methods",
    icon=":material/search_insights:",
)


contact = st.Page(
    page="views/contact.py",
    title="Contact",
    icon=":material/alternate_email:",
)

# Navigation
pg = st.navigation(
    {
        "Insights": [homepage, task_details],
        "Configuration": [custom_extraction_method, default_values_with_env],
        "Contact": [contact],
    }
)

st.logo(str(settings.PROJECT_DIR / ".." / "docs" / "images" / "logo.png"))

st.sidebar.markdown(
    "Made with :material/favorite: by [Tendai](https://github.com/t-charura)"
)


if __name__ == "__main__":
    pg.run()
