from typing import Any, Generic, TypeVar
from src.pipeline.base_pipeline import BasePipeline

T = TypeVar('T')

class DataPipelineInterface(Generic[T]):
    '''
    # this interface provides the interface for data pipeline push and pull method.
    # based on the principle of Depeency Inversion Principle.
    '''
    def __init__(
        self,
        pipeline: BasePipeline, # Upcasting!
        object: T, # object
        push_only: bool = True,
    ) -> None:
        
        self.push_only = push_only
        return

    def push(
        self,
        key : str,
    ) -> None:
        if (self.push_only):
            # do actual thing
            return        
        return
    
    def pop(
        self,
        key : str,    
    ) -> None:
        if not self.push_only:
            # do actual thing
            return        
        return
