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
        self.est_transcript_tokens = self._estimate_tokens()
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

    def _estimate_tokens(self) -> int:
        """
        Estimate the number of tokens in the transcript. Assumes 1 token = 4 characters

        Returns:
            Estimated number of tokens
        """
        char_count = len(self.transcript)
        return char_count // 4

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

    def get_prompt(self) -> str:
        """
        Return the final prompt including the transcript as a string

        Returns:
            The final prompt
        """
        return self._invoke(self.prompt_template).text

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
            raise typer.Abort("Invalid API key")
        except NotFoundError:
            print(
                f'The model "{llm.model_name}" does not exist or you do not have access to it.\n'
                f"You can find all available models at: https://platform.openai.com/docs/models.\n"
                f"Please update the value in your .env file."
            )
            raise typer.Abort("Invalid model name")

    def extract(self, model_name: str, api_key: str) -> str:
        """
        Use LLM to extract knowledge from transcript

        Args:
            model_name: OpenAI model name to use
            api_key: OpenAI API key

        Returns:
            The summary of the transcript
        """
        llm = utils.initialize_llm(
            model_name=model_name if model_name else settings.OPENAI_MODEL_NAME,
            api_key=api_key,
        )
        print(f"Using: [green bold]{llm.model_name}[/green bold]\n")

        return self._extract_knowledge(llm=llm)
