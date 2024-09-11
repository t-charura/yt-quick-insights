import streamlit as st

from yt_quick_insights.frontend import components
from yt_quick_insights.task import TaskDetails, tasks


def display_title_and_description():
    st.title(":material/search_insights: Extraction Methods")
    st.subheader("What are Extraction Methods?")
    st.markdown(
        """
        Extraction Methods are specialized instructions designed to efficiently summarize and analyze video content.
        Suitable for various content types, including:
       - General summaries of key points
       - Comprehensive podcast overviews
       - Extraction of specific action steps and recommendations
       - Compilation of resources mentioned in the video

        To get started:
        - Select an appropriate extraction method from our available options. View all options below.
        - For custom requirements, refer to the [Custom Extraction Method](/yaml_file) page.
        """
    )
    st.divider()


def display_task_details():
    st.subheader("Available Extraction Methods")
    task = st.selectbox(
        "Extraction Method",
        TaskDetails,
        format_func=components.format_dropdown_label,
        index=components.default_index,
        label_visibility="collapsed",
    )

    if task:
        st.markdown(tasks.get(task.value))


def render_task_details():
    """Create task details page structure."""
    display_title_and_description()
    display_task_details()


render_task_details()
