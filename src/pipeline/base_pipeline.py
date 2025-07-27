from queue import Queue
from typing import Dict, Any, TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar("T")

class BasePipeline(ABC, Generic[T]):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def push(
        self,
        *args,
        **kwargs,
    ) -> bool:
        raise NotImplementedError
        
    @abstractmethod
    def pop(
        self,
        *args,
        **kwagrs,
    ) -> T | None:
        raise NotImplementedError
