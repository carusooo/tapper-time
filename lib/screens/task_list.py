import logging
from typing import List
from PIL import Image,ImageDraw

from ..service.core import Task, TaskService
from . import core

class TaskListScreen(core.Screen):
    tasks: List[Task]
    project_id: int
    task_position = 0
    task_service: TaskService
    app: object

    def __init__(self, app: core.App, task_service):
        self.layout = {
            'taskPos0': core.Element(
                    x_start=0, x_end=core.SCREEN_WIDTH,
                    y_start=0, y_end=core.Y4,
                    index=0,
                    click=self.click_task),
            'taskPos1': core.Element(
                    x_start=0, x_end=core.SCREEN_WIDTH,
                    y_start=core.Y4, y_end=core.Y4*2,
                    index=1,
                    click=self.click_task),
            'taskPos2': core.Element(
                    x_start=0, x_end=core.SCREEN_WIDTH,
                    y_start=core.Y4*2, y_end=core.Y4*3,
                    index=2,
                    click=self.click_task),
            'upButton': core.Element(
                    x_start=0, x_end=core.X3,
                    y_start=core.Y4*3, y_end=core.SCREEN_HEIGHT,
                    click=self.up,
                    text='⬆'),
            'refreshButton': core.Element(
                    x_start=core.X3, x_end=core.X3*2,
                    y_start=core.Y4*3, y_end=core.SCREEN_HEIGHT,
                    click=self.refresh,
                    text='🔄'),
            'downButton': core.Element(
                    x_start=core.X3*2, x_end=core.SCREEN_WIDTH,
                    y_start=core.Y4*3, y_end=core.SCREEN_HEIGHT,
                    click=self.down,
                    text='⬇'),
        }
        self.app = app
        self.task_service = task_service
        self.tasks = self.task_service.get_tasks()
        logging.info('Retrieved %d tasks', len(self.tasks))

    def draw(self) -> Image:
        image = Image.new("1", (core.SCREEN_WIDTH, core.SCREEN_HEIGHT),0xFF)
        draw = ImageDraw.Draw(image)

        for i, task in enumerate(self.tasks[self.task_position:self.task_position+3]):
            e = self.layout[f'taskPos{i}']
            draw.multiline_text((e.x_start, e.y_start), task.content, font=core.font15)
        buttons = [self.layout['refreshButton']]
        if self.task_position > 0:
            buttons.append(self.layout['upButton'])
        if len(self.tasks) > self.task_position+3:
            buttons.append(self.layout['downButton'])
        for e in buttons:
            draw.text(core.center(e), e.text, font=core.emojiFont, anchor='mm')
        return image

    def click_task(self, pos):
        self.task_service.current_task = self.tasks[pos + self.task_position]
        return self.app.task_timer

    def up(self):
        if self.task_position > 0:
            self.task_position -= 3
            logging.info('Updating task to %d', self.task_position)
        return self

    def down(self):
        if len(self.tasks) > self.task_position+3:
            self.task_position += 3
            logging.info('Updating task to %d', self.task_position)
        return self

    def refresh(self):
        self.task_position = 0
        self.tasks = self.task_service.get_tasks()
        return self

    def handle_click(self, point: core.Point) -> core.Screen:
        for k, e in self.layout.items():
            if core.within(point, e):
                logging.info('Pressed %s', k)
                if e.index < 0:
                    return e.click()
                else:
                    return e.click(e.index)
        logging.info('No element @ %s', point)
        return self
