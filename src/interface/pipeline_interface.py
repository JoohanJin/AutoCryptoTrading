from typing import Any, Generic, TypeVar
from pipeline.base_pipeline import BasePipeline
from logger.set_logger import operation_logger


T = TypeVar('T')


class PipelineController(Generic[T]):
    '''
    # this interface provides the interface for data pipeline push and pull method.
    # based on the principle of Depeency Inversion Principle.
    '''
    def __init__(
        self,
        pipeline: BasePipeline,  # Upcasting!
        push_only: bool = True,
    ) -> None:
        '''
        - func __init__():
            - Get the actual pipeline.
            - Get the push_only variable so that we can add control of the side. (uni-directional)
        '''
        # Let the programmer decides which operation to be used.
        self.push_only = push_only
        self.pipeline: BasePipeline = pipeline

        operation_logger.info(
            f"{__name__} - pipelineController has been generated."
        )
        return

    def push(
        self,
        object: T,  # object
        key : str,
    ) -> bool:
        '''
        '''
        if (self.push_only):
            # actual pipeline operation.
            try:
                self.pipeline.push(object)
                return True
            except Exception as e:
                operation_logger.warning(
                    f"{__name__} - Unknown Error has been occured. Unsuccessful Push."
                )
                return False

        operation_logger.critical(
            f"{__name__} - Not Authorized Behavior. You cannot push the data from this side."
        )
        raise PermissionError  # ! raise the custom exception

    def pop(
        self,
        key : str,
    ) -> T | None:
        '''
        '''
        if not self.push_only:
            try:
                data: T | None = self.pipeline.pop()
                if data:
                    return data
            except Exception as e:
                # ! raise CustomException
                operation_logger.warning(
                    f"{__name__} - Unknown Error has been occured. Unsuccessful Pop."
                )
                raise  # ! raise the custom exception

        operation_logger.critical(
            f"{__name__} - Not Authorized Behavior. You cannot pop the data from this side."
        )
        raise PermissionError  # ! raise the custom exception


# Testing Code
if __name__ == "__main__":
    print("Done!")
