from email.mime import application
import unittest.mock
import pytest

from app import Application
from lib.screens.task_list import TaskListScreen
from lib.service import core

TASK = core.Task(content='task content 1', id='1', completed=False)
TASKS = [ TASK ]

@pytest.fixture
def mock_service(monkeypatch):
    "Create the mock task service"
    service_mock = unittest.mock.Mock(spec=core.TaskService)
    service_mock.return_value.get_tasks.return_value = TASKS
    service_mock.current_task = TASK
    monkeypatch.setattr("lib.service.todoist.Todoist", service_mock)
    return service_mock

@pytest.fixture
def mock_application(monkeypatch):
    "Create a mock application instance"
    application_mock = unittest.mock.Mock(spec=Application)
    monkeypatch.setattr("app.Application", application_mock)
    return application_mock

@pytest.fixture
def mock_task_list(monkeypatch):
    "Create a mock task list screen"
    task_list_screen_mock = unittest.mock.Mock(spec=TaskListScreen)
    monkeypatch.setattr("lib.screens.task_list.TaskListScreen", task_list_screen_mock)
    return task_list_screen_mock
