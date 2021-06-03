import abc
from abc import ABC
from typing import List
import pandas as pd


class InputConnector(ABC):
    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def open() -> pd.DataFrame:
        pass

class CsvInputConnector(InputConnector):
    def __init__(self, file_path:str, colnames:List=None):
        self._file_path = file_path
        self._colnames = colnames

    @property
    def file_path(self):
        return self._file_path

    def open(self) -> pd.DataFrame:
        if self._colnames:
            return pd.read_csv(self._file_path, names=self._colnames)
        else:
            return pd.read_csv(self._file_path)