import streamlit as st

st.title(":material/text_snippet: Default Values with `.env` File")
with st.container(border=True):
    st.subheader("Why create a `.env` file?")
    st.markdown(
        """
        - Securely store your OPENAI_API_KEY. 
        Eliminating the need to copy and paste your API key every time you run the app.
        - Set your favorite OpenAI model as default.
        - The app will automatically detect and utilize the API key and model name as defaults.
        """
    )

with st.container(border=True):
    st.subheader("How to create a `.env` file?")
    st.markdown(
        """        
        1. Create a `.env` file in the following directory: `~/.insights/.env`
        2. Add the following variables to the file:
    
        ``` properties
        OPENAI_API_KEY=YOUR_OPENAI_API_KEY
        OPENAI_MODEL_NAME=gpt-4.1-mini
        ```
    
        If you're unsure about the correct location for the `.env` file on your system, use the following command:
    
        ``` bash
        insights env-location
        ```
    
        For a comprehensive list of available OpenAI model names, 
        please refer to the [official documentation](https://platform.openai.com/docs/models).
        """
    )
