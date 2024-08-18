from enum import Enum
from unittest.mock import patch

import pytest

from yt_quick_insights.task import TaskManager


@pytest.fixture
def default_tasks():
    return {"task1": "Description 1", "task2": "Description 2"}


@pytest.fixture
def user_tasks():
    return {"task2": "User Description 2", "task3": "Description 3"}


@pytest.fixture
def merged_tasks():
    return {
        "task1": "Description 1",
        "task2": "User Description 2",
        "task3": "Description 3",
    }


def test_init(default_tasks, user_tasks):
    with patch(
        "yt_quick_insights.utils.load_yaml_file",
        return_value=default_tasks,
    ):
        with patch.object(TaskManager, "_load_user_tasks", return_value={}):
            tm = TaskManager()
            assert tm.default_tasks == default_tasks
            assert tm.user_tasks == {}
            assert tm.tasks == default_tasks


def test_load_user_tasks(user_tasks):
    with patch("yt_quick_insights.utils.load_yaml_file", return_value=user_tasks):
        tm = TaskManager()
        assert tm._load_user_tasks() == user_tasks


def test_merge_tasks(default_tasks, user_tasks, merged_tasks):
    with patch(
        "yt_quick_insights.utils.load_yaml_file",
        return_value=default_tasks,
    ):
        tm = TaskManager()
        tm.user_tasks = user_tasks
        assert tm._merge_tasks() == merged_tasks


def test_create_task_enum(merged_tasks):
    with patch("yt_quick_insights.utils.load_yaml_file", return_value=merged_tasks):
        tm = TaskManager()
        task_enum = tm.create_task_enum()
        assert isinstance(task_enum, type(Enum))
        assert set(task_enum.__members__.keys()) == set(merged_tasks.keys())
