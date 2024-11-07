import streamlit as st

from yt_quick_insights.frontend import components
from yt_quick_insights.task import ExtractionMethods, available_extraction_methods


def display_title_and_description():
    st.title(":material/search_insights: Extraction Methods")
    with st.container(border=True):
        st.subheader("What are Extraction Methods?")
        st.markdown(
            """
            Extraction Methods are specialized instructions designed to efficiently summarize and analyze video content.
            Based on the content of the video, select an appropriate extraction method.
            
            Overview of all available extraction methods:
            - **Extensive Summary**: Generate long and extensive summaries with lots of details        
            - **General Summary**: Default, can be used for any type of content
            - **How To Extraction**: For how to videos, Guides and tutorials
            - **Knowledge Extraction**: For informational videos to understand a topic
            - **Podcast Summary**: For podcast and discussions
            - **Resource Extraction**: Quick overview of all resources mentioned in the video
            - **Short Summary**: Summary of 3-6 bullet points
    
            To get started:
            - Select an appropriate extraction method from our available options. View all options in detail below.
            - For custom requirements, refer to the [Custom Extraction Method](/yaml_file) page.
            """
        )


def display_extraction_methods():
    with st.container(border=True):
        st.subheader("Available Extraction Methods")
        task = st.selectbox(
            "Extraction Method",
            ExtractionMethods,
            format_func=components.format_dropdown_label,
            index=components.default_index,
            label_visibility="collapsed",
        )

        if task:
            st.markdown(available_extraction_methods.get(task.value))


def render_extraction_methods():
    """Create task details page structure."""
    display_title_and_description()
    display_extraction_methods()


render_extraction_methods()
