<p align="center">
  <img src="docs/images/banner.png"  alt="project-banner">
</p>

*YouTube Quick Insights is a CLI tool designed to extract meaningful insights from YouTube videos without watching them.
Download the YouTube transcript, integrate it into a ready-to-use prompt, and use it with your favorite LLM.*

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
  <a href='#roadmap'>Roadmap</a> •
  <a href='#contact'>Contact</a>
</p>


---

---

## About the Project

### Key Features

* **Prompt Generation:** Generate and download ready-to-use prompts as txt files to help you gain insights from YouTube
  video content.
* **Prompt Customization:** Tailor prompts to fit various needs such as basic summaries, extracting action steps,
  summarizing podcasts, or extracting resources.

### Why it's valuable?

* **Save Time:** Obtain critical information from videos without spending time watching them.
* **Flexibility:** Customize the prompt generation process according to your needs, ensuring that you get the insights
  that matter most to you.
* **Ease of Use & Cost-Free:** CLI is easy to use and doesn't require an OpenAI API key, making it completely free with
  no additional costs.

## Installation

**Recommended:** Create and activate
a [virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments) before installing the
tool.

**Using pip**

``` bash
pip install yt-quick-insights
```

**Using poetry**

``` bash
poetry add yt-quick-insights
```

To verify that everything works and to see all available commands

``` bash
insights --help
```

## Usage

Download the prompt in txt format in your current working directory.

``` bash
insights download https://www.youtube.com/watch?v=VIDEO_ID
```

Customize the prompt to your needs with different tasks by using the `-t` flag.

To see all available tasks run: `insights available-tasks`

Additional you can add background information for the video by using the `-b` flag. Example:

``` bash
insights download https://www.youtube.com/watch?v=VIDEO_ID -t podcast_summary -b "In this podcast episode 4 guests and a moderator talk about the future of AI."
```

### Configure your own task

Create a yaml file in your home directory under `~/.insights/task_details.yml`.

``` yaml
custom: |
  Create your own custom task here.
  You can use multiple lines to describe your task.
  
default: |
  If you add a task name 
  that already exists in the default tasks, 
  it will be overwritten.
```

Not sure where to create the yaml file in your system?

``` bash
insights yaml-location
```

You can use your custom task by running the download command with the `-t` option

``` bash
insights download https://www.youtube.com/watch?v=VIDEO_ID -t custom
```

To see all currently available tasks

``` bash
insights available-tasks
```

## Limitations

* **Transcript Quality:** YouTube's auto-generated transcripts can contain errors.
* **AI Imperfections:** LLMs are not perfect
* **Technical Requirements:** Basic command-line knowledge is needed.

## Roadmap

* [x] Publish on PyPI
* [ ] Add option to summarize the transcript directly insight the CLI using an LLM.
* [ ] Create a web-based interface for non-technical users.

## Contact

* **Website:** https://charura.com
* **Email:** tendai@charura.com
* **Github:** [t-charura](https://github.com/t-charura)
