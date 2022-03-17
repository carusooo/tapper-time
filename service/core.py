from abc import ABC, abstractmethod

from dataclasses import dataclass


@dataclass
class Task:
    content: str
    id: int
    completed: bool

class TaskService(ABC):
    @abstractmethod
    def get_tasks(self) -> list[Task]:
        pass
