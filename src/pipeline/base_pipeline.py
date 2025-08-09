from queue import Queue
from typing import Dict, Any
from abc import ABC, abstractmethod

class BasePipeline(ABC):
    @abstractmethod
    def __init__(self) -> None:
        return

    @abstractmethod
    def push(
        self,
        *args,
        **kwargs,
    ):
        return False
    
    @abstractmethod
    def pop(
        self,
        *args,
        **kwagrs,
    ):
        return
    