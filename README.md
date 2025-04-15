<p align="center">
  <img src="docs/images/banner.png"  alt="project-banner">
</p>

*YouTube Quick Insights is a Python webapp designed to help users rapidly extract insights from YouTube content.
This application enables you to summarize videos, extract key information,
and analyze entire playlists without spending hours watching them.*

<p align="center">
	<img src="https://img.shields.io/github/license/t-charura/yt-quick-insights?style=default&logo=opensourceinitiative&logoColor=white&color=5bb8fc" alt="license">
	<img src="https://img.shields.io/github/last-commit/t-charura/yt-quick-insights?style=default&logo=git&logoColor=white&color=5bb8fc" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/t-charura/yt-quick-insights?style=default&logo=python&logoColor=white&color=5bb8fc" alt="repo-top-language">
	<img src="https://img.shields.io/pypi/v/yt-quick-insights?style=default&logo=pypi&logoColor=white&color=5bb8fc" alt="PyPI - Version">
	<img src="https://img.shields.io/github/actions/workflow/status/t-charura/yt-quick-insights/.github%2Fworkflows%2FCI.yaml?logo=githubactions" alt="github-actions">
</p>


<p align="center">
  <a href='#about-the-project'>About the Project</a> •
  <a href='#installation'>Installation</a> •
  <a href='#usage'>Usage</a> •
  <a href='#limitations'>Limitations</a> •
  <a href='#known-issues'>Known Issues</a> •
  <a href='#roadmap'>Roadmap</a> •
  <a href='#contact'>Contact</a>
</p>


---

## About the Project

With the overwhelming volume of content on YouTube, finding relevant information can be time-consuming and inefficient.
YouTube Quick Insights solves this by instantly summarizing videos, extracting key information, and analyzing entire
playlists.
This AI-powered app saves time and enhances knowledge retention, making learning from YouTube content easier and more
effective.
You can also read more about this project in my [Medium blog post](https://medium.com/@tendai.charura/instant-youtube-insights-skip-the-viewing-keep-the-learning-f42404729e58).

### Key Features

- **🎥 Video Insights**: Extract relevant information from individual YouTube videos using various extraction methods.
- **❓ Question-Based Insights**: Ask specific questions about a video to get targeted information.
- **📚 Playlist Analysis**: Analyze each video in a playlist and generate a comprehensive summary of the playlist's
  content.
- **🔧 Flexible Extraction Methods**: Choose from pre-defined extraction methods or create custom ones to suit your
  needs.

### Why it's valuable?

- **⏱️ Time-Saving**: Obtain critical information from videos without spending hours watching them.
- **🎛️ Customizable Analysis**: Tailor the extraction process to focus on specific aspects of the content.
- **📈 Scalable**: Effortlessly analyze individual videos or entire playlists.
- **🧠 Enhanced Learning & Retention**: Use generated summaries for personal notes to review content later, improving
  long-term retention.
- **🖱️ Ease of Use**: Simple and user-friendly web interface.

### Build with

<p>
  <img src="docs/images/python.png" width="30" alt="python-logo" align="top">
  <a href="https://www.python.org/">Python</a>
</p>

<p>
  <img src="docs/images/langchain.png" width="30" alt="langchain-logo" align="top">
  <a href="https://github.com/langchain-ai/langchain">LangChain</a>
</p>

<p>
  <img src="docs/images/streamlit.png" width="33" alt="streamlit-logo" align="top">
  <a href="https://github.com/streamlit/streamlit">Streamlit</a>
</p>

## Installation

**Recommended:** Create and activate
a [virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments) before installing the
tool.

**Using pip**

```bash
pip install yt-quick-insights
```

**Using poetry**

```bash
poetry add yt-quick-insights
```

To verify that everything works

```bash
insights --help
```

## Usage

To launch the application, open your terminal and run the following command:

```bash
insights run
```

The webapp should open automatically in your default browser. If not, navigate to:
`http://localhost:8501`.

<img src="https://github.com/user-attachments/assets/b02ea88c-09c6-477f-87dc-ff3d329674d8" alt="usage_gif" width="75%">

1. **Enter YouTube URL:** Paste the URL of the YouTube video you want to summarize in the designated field.
2. **Set OpenAI API Key:** You have three options to provide your OpenAI API key:
    - Enter it directly in the designated field
    - Set it in the `.env` file
    - Store the key in an environment variable called: `OPENAI_API_KEY`
3. **Generate Insights:** Click on the "Get Insights" button to start summarizing the video content.

**(Optional Settings)**

1. **Select Extraction Method:** Choose a specific method for extracting information based on the video content,
   defaults to `General Summary`.
2. **Choose OpenAI Model:** Select any available OpenAI model for generating insights, defaults to `gpt-4.1-mini`.

For detailed usage instructions, please refer to the in-app Usage Guide. To set up a `.env` file or create a custom
Extraction Method, navigate to the "Configuration" section in the app's navigation bar.

## Limitations

- Relies on the availability and accuracy of video transcripts.
- Requires an OpenAI API key for operation.
- May not capture visual information or context that isn't described in the audio.
- Only OpenAI LLMs are supported at this time.

## Known Issues

* The YouTube transcript download feature does not work when using a VPN (tested with NordVPN).
    * For more details, refer to this [issue thread](https://github.com/jdepoix/youtube-transcript-api/issues/303).

## Roadmap

- [x] Publish on PyPI
- [x] Transform the CLI into a web app
- [ ] Deploy the web app (Simplify user experience: no need to install locally)
- [ ] Implement parallelization for extracting insights from YouTube Playlists

## Contact

- **🌐 Website:** [https://charura.com](https://charura.com)
- **📧 Email:** tendai@charura.com
- **👨‍💻 GitHub:** [@t-charura](https://github.com/t-charura)

---

<p align="center">
  If you find YouTube Quick Insights helpful, please consider giving it a ⭐️ on GitHub!
</p>
