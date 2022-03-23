from abc import ABC, abstractmethod
from typing import List

from dataclasses import dataclass


@dataclass
class Task:
    content: str
    id: int
    completed: bool

class TaskService(ABC):
    @abstractmethod
    def __init__(self, api_key: str, project_id: str) -> None:
        pass

    @abstractmethod
    def get_tasks(self) -> List[Task]:
        pass
    
    @abstractmethod
    def task_completed(self, task: Task) -> None:
        pass
