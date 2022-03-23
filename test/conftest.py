import pytest
import unittest.mock
from lib.service import core

TASKS = [
    core.Task(content='task content 1', id='1', completed=False)
]

@pytest.fixture
def mock_service(monkeypatch):
    "Create the mock task service"
    service_mock = unittest.mock.Mock(spec=core.TaskService)
    service_mock.return_value.get_tasks.return_value = TASKS
    monkeypatch.setattr("lib.service.todoist.Todoist", service_mock)
    return service_mock
