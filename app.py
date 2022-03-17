import logging
import threading
import time

from lib.screens import core, task_list, task_timer, timer_done
from lib.service import todoist

logging.basicConfig(level=logging.DEBUG)

POMODORO_DURATION_S = 28*60

class Application(core.App):
    service: todoist.Todoist
    current_screen: core.Screen = None
    __thread: threading.Thread
    tasks_changed: bool

    def __init__(self, api, project_id):
        self.service = todoist.Todoist(api_key=api, project_id=project_id)
        self.__redraw = False
        self.__task_list = task_list.TaskListScreen(self, self.service)
        self.__task_timer = task_timer.TaskTimerScreen(self, self.service)
        self.__timer_done = timer_done.TimerDoneScreen(self, self.service)
        self.__thread = None
        self.__timer_end_time = 0


    def start(self):
        self.tasks_changed = False
        self.current_screen = self.task_list
        return self.current_screen.draw()

    def handle_click(self, click):
        # The XY are reported for portrait orientation and with (0,0) in the lower left
        point = core.Point(y=(core.SCREEN_HEIGHT-click.X[0]), x=click.Y[0], s=click.S[0])
        self.current_screen = self.current_screen.handle_click(point)
        return self.current_screen.draw()

    def draw(self):
        return self.current_screen.draw()

    @property
    def task_list(self) -> core.Screen:
        if self.__thread and self.__thread.is_alive():
            self.__thread.cancel()
        if self.tasks_changed:
            self.__task_list.refresh()
        return self.__task_list

    @property
    def task_timer(self) -> core.Screen:
        self.__timer_end_time = time.time() + POMODORO_DURATION_S
        self.__task_timer.end_time = self.__timer_end_time
        self.update_timer()
        return self.__task_timer

    @property
    def timer_done(self) -> core.Screen:
        return self.__timer_done

    @property
    def redraw(self):
        redraw = self.__redraw
        self.__redraw = False
        return redraw

    def request_redraw(self):
        self.__redraw = True

    def update_timer(self):
        if time.time() >= self.__timer_end_time:
            self.current_screen = self.timer_done
            self.request_redraw()
        self.__thread = threading.Timer(60, self.update_timer)
        self.__thread.start()
        self.request_redraw()
