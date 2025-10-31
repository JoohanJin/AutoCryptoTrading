import sys
from pathlib import Path
from dotenv import load_dotenv

from manager.system_manager import SystemManager
from logger.set_logger import operation_logger


def main():
    try:
        # ? Since __init__() for every class will activate them, no need to do anything here.
        project_root = Path(__file__).resolve().parents[1]
        load_dotenv(project_root / ".env")

        main_system_manager: SystemManager = SystemManager()
        operation_logger.info(
            f"{main_system_manager} has been started."
        )
    except RuntimeError as e:
        operation_logger.critical(
            f"{__name__}: function main() has raised an RuntimeError: {str(e)}"
        )
        sys.exit(1)
    except Exception as e:
        operation_logger.critical(
            f"{__name__}: function main() has raised an Unexpected error starting the system: {str(e)}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
