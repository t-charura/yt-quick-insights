import streamlit as st

st.title(":material/settings: Custom Extraction Method")

st.subheader("Why use a custom extraction method?")
st.markdown(
    """
    While our standard extraction methods provide comprehensive summaries of entire videos, 
    custom extraction methods offer the flexibility to focus on specific content within the video
    which is relevant to you.

    Example Use Case:
    For a 2-hour podcast on productivity, you might create a custom extraction method to:

    * Extract and summarize all aspects related to developing an enhanced morning routine 
      for increased productivity.
    """
)
st.subheader("How to create a custom extraction method?")
st.markdown(
    """
    1. Create a YAML file named `task_details.yml` in the following directory: `~/.insights/`
    2. Structure your YAML file as follows:

    ``` yaml
    custom: |
      Describe your custom extraction method here.
      You can use multiple lines for detailed instructions.
      Choose a unique name for your extraction method or use 'custom'.

    default: |
      Note: If you use an extraction method name that already exists,
      it will override the existing method.
    ```

    To locate the correct directory for your YAML file, use the following command:

    ``` bash
    insights yaml-location
    ```
    
    For a comprehensive list of available Extraction Methods, 
    click [here](/extraction_methods#available-extraction-methods).
    """
)
