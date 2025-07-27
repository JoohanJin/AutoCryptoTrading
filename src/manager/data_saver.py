import os
import time
import pandas as pd
from logger.set_logger import operation_logger


class DataSaver:
    def __init__(self):
        # Set the base directory to the correct location of 'src'
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.data_dir = os.path.join(self.base_dir, "data")  # Absolute path to 'src/data'

    @property
    def _output_path(self):
        # Construct the absolute path for the CSV file
        return os.path.join(self.data_dir, f"{time.strftime('%Y-%m-%d', time.localtime(time.time()))}.csv")

    def write(self, data: pd.DataFrame):
        try:
            # Ensure the data directory exists
            os.makedirs(self.data_dir, exist_ok=True)

            # Validate the input data
            if data is None or not isinstance(data, pd.DataFrame):
                operation_logger.error(f"{__name__} - TypeError - DataSaver.write: Provided data is not a Pandas DataFrame.")
                return
            if data.empty:
                operation_logger.error(f"{__name__} - No Data in DataSaver.write: Provided data is empty after dropna.")
                return

            # Drop NaN values
            data.dropna(inplace=True)

            # Check if the CSV file already exists
            if os.path.isfile(self._output_path):
                data.to_csv(
                    self._output_path,
                    index=True,
                    header=False,  # Append without writing header
                    index_label="timestamp",
                    mode="a",  # Append mode
                    encoding="utf-8",
                )
            else:
                # Write a new file with the header
                data.to_csv(
                    self._output_path,
                    index=True,
                    index_label="timestamp",
                    encoding="utf-8",
                )

        except FileNotFoundError as e:
            operation_logger.error(f"{__name__} - FileNotFoundError in DataSaver.write: {str(e)}")
        except PermissionError as e:
            operation_logger.error(f"{__name__} - PermissionError in DataSaver.write: {str(e)}")
        except AttributeError as e:
            operation_logger.error(f"{__name__} - AttributeError in DataSaver.write: {str(e)}")
        except OSError as e:
            operation_logger.error(f"{__name__} - OSError in DataSaver.write: {str(e)}")
        except Exception as e:
            operation_logger.error(f"{__name__} - Unexpected error in DataSaver.write: {str(e)}")


# Test Code Run Zone
if __name__ == "__main__":
    # Test the DataSaver class
    __test_drive = DataSaver()

    # Print the output path to verify correctness
    print(__test_drive._output_path())

    # Example of writing data (you can adjust this for testing)
    test_data = pd.DataFrame(
        {
            "value1": [1, 2, None, 4],
            "value2": [5, 6, 7, None],
        },
        index=pd.date_range(start="2024-12-25", periods=4, freq="D"),
    )
    __test_drive.write(test_data)
