import pytest

import PIL

import app

PROJECT_ID = 'project_id'
API_KEY = 'api_key'
POMODORO_DURATION = 25

def test_app_create(mock_service):
    "Test creating an app instance"
    test_app = app.Application(API_KEY, PROJECT_ID, POMODORO_DURATION)
    assert test_app
    mock_service.assert_called_with(API_KEY, PROJECT_ID)

def test_app_start(mock_service):
    "Test starting an app instance"
    test_app = app.Application(API_KEY, PROJECT_ID, POMODORO_DURATION)
    screen = test_app.start()
    assert screen
    assert isinstance(screen, PIL.Image.Image)

def test_task_complete(mock_task_list):
    "Test completing a task refreshes the list"
    test_app = app.Application(API_KEY, PROJECT_ID, POMODORO_DURATION)
    test_app.start()
    test_app.tasks_changed = True
    mock_screen = test_app.task_list
    mock_screen.refresh.assert_called_once()

def test_task_cancelled(mock_task_list):
    "Test cancelling a task does not refresh the list"
    test_app = app.Application(API_KEY, PROJECT_ID, POMODORO_DURATION)
    test_app.start()
    mock_screen = test_app.task_list
    mock_screen.refresh.assert_not_called()
