import string
from typing import List

from todoist_api_python.api import TodoistAPI

from . import core

class Todoist(core.TaskService):
    api_key: string
    project_id: string
    __current_task: core.Task
    _api: TodoistAPI

    def __init__(self, api_key: str, project_id: str) -> None:
        super(Todoist, self).__init__(api_key=api_key, project_id=project_id)
        self.api_key = api_key
        self.project_id = project_id
        self._api = TodoistAPI(api_key)
        self.__current_task = None

    def get_tasks(self) -> List[core.Task]:
        return self._api.get_tasks(project_id=self.project_id)

    def task_completed(self, task: core.Task) -> None:
        self._api.close_task(task_id=task.id)

    @property
    def current_task(self) -> core.Task:
        return self.__current_task

    @current_task.setter
    def current_task(self, task: core.Task) -> None:
        self.__current_task = task
