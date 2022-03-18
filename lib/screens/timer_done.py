import logging

from PIL import Image,ImageDraw

from ..service.core import Task, TaskService
from . import core

class TimerDoneScreen(core.Screen):
    task: Task
    app: core.App
    service: TaskService

    def __init__(self, app: core.App, service):
        self.layout = {
        'prompt': core.Element(
                x_start=0, x_end=core.SCREEN_WIDTH,
                y_start=0, y_end=core.Y4*2,
                index=0,
                click=self.noop),
        'taskDesc': core.Element(
                x_start=0, x_end=core.SCREEN_WIDTH,
                y_start=core.Y4*2, y_end=core.Y4*3,
                index=2,
                click=self.noop),
        'cancelButton': core.Element(
                x_start=0, x_end=core.X2,
                y_start=core.Y4*3, y_end=core.SCREEN_HEIGHT,
                click=self.cancel,
                text='🚫'),
        'doneButton': core.Element(
                x_start=core.X2, x_end=core.SCREEN_WIDTH,
                y_start=core.Y4*3, y_end=core.SCREEN_HEIGHT,
                click=self.done,
                text=u'\u2611'),
        }
        self.app = app
        self.task = service.current_task
        self.service = service

    def draw(self) -> Image:
        self.task = self.service.current_task
        image = Image.new("1", (core.SCREEN_WIDTH, core.SCREEN_HEIGHT),0xFF)
        draw = ImageDraw.Draw(image)
        timer = self.layout['prompt']
        draw.text((timer.x_end//2, timer.y_end//2),
                   'Did you complete?', font=core.font24, anchor='mm', align='center')
        desc = self.layout['taskDesc']
        draw.multiline_text((desc.x_start, desc.y_start), self.task.content, font=core.font15)
        buttons = [self.layout['cancelButton'], self.layout['doneButton']]
        for e in buttons:
            draw.text(core.center(e), e.text, font=core.emojiFont, anchor='mm')
        return image

    def handle_click(self, point: core.Point) -> core.Screen:
        if not point:
            return self
        for k, e in self.layout.items():
            if core.within(point, e):
                logging.info('Pressed %s', k)
                if e.index < 0:
                    return e.click()
                else:
                    return e.click(e.index)
        logging.info('No element @ %s', point)
        return self

    def done(self) -> core.Screen:
        self.service.task_completed(self.task)
        self.app.tasks_changed = True
        return self.app.task_list

    def cancel(self) -> core.Screen:
        return self.app.task_list

    def noop(self) -> core.Screen:
        return self
