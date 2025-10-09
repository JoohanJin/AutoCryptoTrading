from manager.system_manager import SystemManager
from logger.set_logger import operation_logger
from dotenv import load_dotenv


def main():
    try:
        # ? Since __init__() for every class will activate them, no need to do anything here.
        # TODO: but expliciti activation should be better. In the near future.
        load_dotenv()
        main_system_manager: SystemManager = SystemManager()
        operation_logger.info(
            f"{main_system_manager} has been started."
        )
    except Exception as e:
        operation_logger.critical(
            f"{__name__}: function main() has raised an Unexpected error starting the system: {e}"
        )
        return


if __name__ == "__main__":
    main()
