from enum import Enum
from typing import Type

from yt_quick_insights import utils
from yt_quick_insights.config import settings


class TaskManager:
    """
    This class provides functionality to load and merge the default and user-defined tasks.
    Additionally, it creates an Enum object for all tasks.
    """

    def __init__(self, file_name: str = "task_details.yml"):
        """
        Initialize the TaskManager class

        Args:
            file_name: The name of the YAML file containing the default and user tasks.
        """
        self.file_name = file_name
        self.default_tasks = utils.load_yaml_file(
            file_name=self.file_name, directory=settings.PROJECT_DIR / "data"
        )
        self.user_tasks = self._load_user_tasks()
        self.tasks = self._merge_tasks()

    def _load_user_tasks(self) -> dict[str, str]:
        """
        Load user-defined tasks from a YAML file.

        Returns:
            A dictionary of user-defined tasks.
        """
        try:
            return utils.load_yaml_file(self.file_name, settings.HOME_DIR / ".insights")
        except FileNotFoundError:
            return {}

    def _merge_tasks(self) -> dict[str, str]:
        """
        Merge the default tasks with the user-defined tasks.
        User-defined tasks override the default tasks.

        Returns:
            A merged and sorted dictionary of tasks.
        """
        return dict(sorted({**self.default_tasks, **self.user_tasks}.items()))

    def create_task_enum(self) -> Type[Enum]:
        """
        Create an Enum object with the keys of the tasks dictionary.

        Returns:
            An Enum object with the keys of the tasks dictionary.
        """
        return Enum("TaskDetails", {key: key for key in self.tasks.keys()})


task_manager = TaskManager()
tasks = task_manager.tasks

TaskDetails = task_manager.create_task_enum()
