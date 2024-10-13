import json, csv, time, os
import pandas as pd

class DataSaver:
    @property
    def _output_path(self):
        return f"data/{time.strftime('%Y-%m-%d', time.localtime(time.time()))}.csv"

    def write(
        self,
        data: pd.DataFrame,
    ):
        data.dropna(inplace=True)
        if os.path.isfile(self._output_path):
            data.to_csv(
                self._output_path,
                index = True,
                header = False,
                index_label = "timestamp",
                mode = "a",
                encoding = "utf-8",
            )
        else: # no output file
            data.to_csv(
                self._output_path,
                index = True,
                encoding = "utf-8",
            )
        return
    

if __name__ == "__main__":
    __test_drive = DataSaver()
    print(__test_drive._output_path())