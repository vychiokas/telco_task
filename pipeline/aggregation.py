from pipeline.data_source import InputConnector
import pandas as pd
from datetime import date

class Aggregator():
    def __init__(self, data: pd.DataFrame):
        self._data = data

    def aggregate(self, col_name):

        df = self._data[col_name].value_counts().rename_axis(col_name).reset_index(name="counts")
        df["timestamp"] = pd.to_datetime("now")
        df = df[df[col_name] != col_name]
        return df
