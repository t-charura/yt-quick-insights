from pathlib import Path
from typing import Union

import typer
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSerializable
from openai import AuthenticationError, NotFoundError
from rich import print

from yt_quick_insights import utils
from yt_quick_insights.config import settings


class QuickInsights:
    """
    Please add a docstring here
    """

    def __init__(
        self,
        title: str,
        transcript: str,
        task: str,
        background_information: str,
    ):
        """
        Initialize the class with the video URL, task, background information, and video language.

        Args:
            title: The title of the YouTube video.
            transcript: The transcript of the YouTube video.
            task: Specification on how to summarize the transcript.
            background_information: Additional contextual information about the video.
        """
        self.title = title
        self.transcript = transcript
        self.task = task
        self.background_information = background_information
        self.prompt_template = self._load_prompt_template()

    @staticmethod
    def _load_prompt_template():
        """Load template from YAML file and convert into PromptTemplate"""
        template = utils.load_yaml_file(
            file_name="prompt.yml", directory=settings.PROJECT_DIR / "data"
        )

        return PromptTemplate(
            template=template.get("prompt"),
            input_variables=[
                "video_title",
                "task",
                "background_information",
                "youtube_transcript",
            ],
        )

    def _invoke(
        self, obj_to_invoke: Union[RunnableSerializable, PromptTemplate]
    ) -> Union[AIMessage, PromptValue]:
        """
        Inject variables into the LLM chain or PromptTemplate

        Args:
            obj_to_invoke: LLM chain or prompt template

        Returns:
            The output of the LLM chain or the prompt template
        """
        return obj_to_invoke.invoke(
            {
                "video_title": self.title,
                "task": self.task.rstrip(),
                "background_information": self.background_information,
                "youtube_transcript": self.transcript,
            }
        )

    def download_prompt(self) -> None:
        """
        Save the final prompt to a text file in your current working directory.
        """
        file_name = f"{utils.clean_youtube_video_title(self.title)}.txt"
        prompt = self._invoke(self.prompt_template)
        utils.save_to_file(file_name=file_name, content=prompt.text)

        print(f'File saved at: "{Path.cwd() / file_name}"')

    def _extract_knowledge(self, llm: ChatOpenAI) -> str:
        """
        Build and invoke LLM chain to extract knowledge from transcript

        Args:
            llm: LLM model to use

        Returns
            The summary of the transcript

        Raises:
            AuthenticationError: If OpenAI API key is invalid
            NotFoundError: If the model does not exist, or you do not have access to it
        """
        chain = self.prompt_template | llm

        try:
            return self._invoke(chain).content
        except AuthenticationError:
            print(
                "Incorrect API key provided!\n"
                "You can find your API key at: https://platform.openai.com/account/api-keys.\n"
                "Please update the value in your .env file."
            )
            raise typer.Abort()
        except NotFoundError:
            print(
                f'The model "{llm.model_name}" does not exist or you do not have access to it.\n'
                f"You can find all available models at: https://platform.openai.com/docs/models\n"
                f"Please update the value in your .env file."
            )
            raise typer.Abort()

    def run(self, model_name: str, api_key: str, save: bool) -> None:
        """
        Extract knowledge from the YouTube video using the LLM model.

        Args:
            model_name: OpenAI model name to use
            api_key: OpenAI API key
            save: whether to save the result as a markdown file
        """
        llm = utils.initialize_llm(
            model_name=model_name if model_name else settings.OPENAI_MODEL_NAME,
            api_key=api_key,
        )
        print(f"Using: [green bold]{llm.model_name}[/green bold]\n")

        result = self._extract_knowledge(llm=llm)

        if save:
            file_name = f"{utils.clean_youtube_video_title(self.title)}.md"
            utils.save_to_file(file_name=file_name, content=result)

        utils.show_markdown_output(result)
