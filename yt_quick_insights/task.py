from enum import Enum
from typing import Type

from yt_quick_insights import utils
from yt_quick_insights.config import settings


class TaskManager:
    """
    This class provides functionality to load and merge the default and user-defined extraction_methods.
    Additionally, it creates an Enum object for all available_extraction_methods.
    """

    def __init__(self, file_name: str = "extraction_methods.yml"):
        """
        Initialize the TaskManager class

        Args:
            file_name: The name of the YAML file containing the default and user extraction_methods.
        """
        self.file_name = file_name
        self.default_tasks = utils.load_yaml_file(
            file_name=self.file_name, directory=settings.PROJECT_DIR / "data"
        )
        self.user_tasks = self._load_user_tasks()
        self.tasks = self._merge_tasks()

    def _load_user_tasks(self) -> dict[str, str]:
        """
        Load user-defined extraction_methods from a YAML file.

        Returns:
            A dictionary of user-defined available_extraction_methods.
        """
        try:
            return utils.load_yaml_file(self.file_name, settings.HOME_DIR / ".insights")
        except FileNotFoundError:
            return {}

    def _merge_tasks(self) -> dict[str, str]:
        """
        Merge the default extraction_methods with the user-defined extraction_methods.
        User-defined extraction_methods override the default extraction_methods.

        Returns:
            A merged and sorted dictionary of available_extraction_methods.
        """
        return dict(sorted({**self.default_tasks, **self.user_tasks}.items()))

    def create_task_enum(self) -> Type[Enum]:
        """
        Create an Enum object with the keys of the available_extraction_methods dictionary.

        Returns:
            An Enum object with the keys of the available_extraction_methods dictionary.
        """
        return Enum("ExtractionMethods", {key: key for key in self.tasks.keys()})


task_manager = TaskManager()
available_extraction_methods = task_manager.tasks

ExtractionMethods = task_manager.create_task_enum()
