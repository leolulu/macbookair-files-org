from abc import ABC,abstractmethod
from typing import List

from models.whisper_task import WhisperTask


class BaseReader(ABC):
    def __init__(self) -> None:
        self.tasks: List[WhisperTask]

    @abstractmethod
    def gen_tasks(self) -> WhisperTask:
        pass