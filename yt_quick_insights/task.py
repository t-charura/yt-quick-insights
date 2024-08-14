from enum import Enum
from typing import Type

from yt_quick_insights import utils


class TaskManager:

    def __init__(self, file_name: str = "task_details.yml"):
        self.file_name = file_name
        self.default_tasks = utils.load_yaml_file(self.file_name)
        self.user_tasks = self._load_user_tasks()
        self.tasks = self._merge_tasks()

    def _load_user_tasks(self) -> dict[str, str]:
        try:
            return utils.load_yaml_file(self.file_name, user_yaml=True)
        except FileNotFoundError:
            return {}

    def _merge_tasks(self) -> dict[str, str]:
        return dict(sorted({**self.default_tasks, **self.user_tasks}.items()))

    def create_task_enum(self) -> Type[Enum]:
        return Enum("TaskDetails", {key: key for key in self.tasks.keys()})


task_manager = TaskManager()
tasks = task_manager.tasks

TaskDetails = task_manager.create_task_enum()
