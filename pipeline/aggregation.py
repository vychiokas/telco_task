from pipeline.data_source import InputConnector
import pandas as pd
from datetime import date

class Aggregator():
    def __init__(self, data: pd.DataFrame):
        self._data = data

    def aggregate(self, col_name):
        

        # customers_service_type_df = self._data.groupby(by=[col_name]).size()
        import pdb
        pdb.set_trace()
        df = self._data[col_name].value_counts().rename_axis(col_name).reset_index(name="counts")
        df["timestamp"] = date.today().strftime("%Y-%m-%dT%H:%M:%S.%f%z")

        return df
        
        # customers_rate_plan_df = self._data.groupby(by=[col_name]).size()
        # dfcrp = customers_rate_plan_df.to_frame()
        # dfcrp["timestamp"] = pd.to_datetime("now", format='%Y-%m-%dT%H:%M:%S.%f%z')
