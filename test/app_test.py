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
    "Test creating an app instance"
    test_app = app.Application(API_KEY, PROJECT_ID, POMODORO_DURATION)
    screen = test_app.start()
    assert screen
    assert isinstance(screen, PIL.Image.Image)
