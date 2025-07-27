from queue import Queue
from typing import Dict, Any
from abc import ABC, abstractmethod

class BasePipeline(ABC):
    @abstractmethod
    def __init__(self) -> None:
        return

    @abstractmethod
    def push_data(
        self,
        *args,
        **kwargs,
    ) -> Any:
        return False
    
    @abstractmethod
    def pop_data(
        self,
        *args,
        **kwagrs,
    ) -> Any:
        return

    