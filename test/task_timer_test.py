from lib.screens import core, task_timer


def center_point(layout_item: core.Element):
    """Returns the center point of an element."""
    def center(p1, p2):
        return (p2-p1)+p1
    return core.Point(
        x=center(layout_item.x_start, layout_item.x_end),
        y=center(layout_item.y_start, layout_item.y_end),
        s=0
    )


def test_task_timer_create(mock_service, mock_application):
    "Test creating a task timer screen"
    timer_screen = task_timer.TaskTimerScreen(mock_application, mock_service)
    assert timer_screen


def test_task_timer_complete(mock_service, mock_application):
    "Test completing a task marks it complete"
    timer_screen = task_timer.TaskTimerScreen(mock_application, mock_service)
    result = timer_screen.handle_click(center_point(timer_screen.layout['doneButton']))
    assert result
    mock_service.task_completed.assert_called_once()
    assert mock_application.tasks_changed is True

def test_task_timer_cancel(mock_service, mock_application):
    "Test canceling a task leaves the task as is"
    timer_screen = task_timer.TaskTimerScreen(mock_application, mock_service)
    result = timer_screen.handle_click(center_point(timer_screen.layout['cancelButton']))
    assert result
    mock_service.task_completed.assert_not_called()
