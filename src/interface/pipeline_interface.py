

from typing import Any


class DataPipelineInterface:
    '''
    # this interface provides the interface for data pipeline push and pull method.
    # based on the principle of Depeency Inversion Principle.
    '''
    def __init__(self) -> None:
        return

    def push(
        self,
        key : str,
        data : Any,
    ) -> None:
        return
    
    def pop(
        self,
        key : str,    
    ) -> None:
        return
