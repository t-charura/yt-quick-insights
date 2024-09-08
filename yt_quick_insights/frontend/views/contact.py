import streamlit as st
from rich.markdown import Markdown


def display_title():
    st.title(":material/alternate_email:  Contact")


def func():
    return st.markdown("Tendai")


def display_contact_details():
    col1, col2 = st.columns(2)

    col1.markdown(
        """
    - :material/code: GitHub: [Tendai](https://github.com/t-charura)
    - :material/language: Website: [https://charura.com/](http://charura.com)
    - :material/mail: Email:  tendai@charura.com
    """
    )

    col2.markdown("Put your AI generated Image here")


def render_contact():
    """Create contact page structure."""
    display_title()
    display_contact_details()


render_contact()
