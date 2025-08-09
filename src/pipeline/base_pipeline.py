from queue import Queue
from typing import Dict, Any, Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar('T')


class BasePipeline(ABC, Generic[T]):
    @abstractmethod
    def __init__(self) -> None:
        return

    @abstractmethod
    def push(
        self,
        *args,
        **kwargs,
    ) -> bool:
        return False

    @abstractmethod
    def pop(
        self,
        *args,
        **kwagrs,
    ) -> T | None:
        return
