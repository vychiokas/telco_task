import pandas as pd
import pdb
import pandera as pa
from .data_source import InputConnector

class DataCheck():

    _FAILURE_CASES_DF_FILE = "data/failure_cases.csv"
    _FAILURE_DF_ROWS_FILE = "data/err_data.csv"
    def __init__(self, in_connector: InputConnector, **kwargs):
        self._in_connector = in_connector
        self._data = None
        self._LOG = kwargs.get("log")
        self._drop_duplicates = kwargs.get("drop_duplicates")
        

    @property
    def in_connector(self):
        return self._in_connector

    @property
    def data(self):
        return self._data

    @property
    def LOG(self):
        return self._LOG
        
        # self._data = pd.read_csv("data/usage.csv", names=["customer_id", "event_start_time", "event_type", "rate_plan_id", "billing_flag_1", "billing_flag_2", "duration", "charge", "month"])
    
    def run(self):
        schema = pa.DataFrameSchema(
        columns={
            "customer_id": pa.Column(pa.Int, [pa.Check.greater_than(0)]),
            "event_start_time": pa.Column(pa.String),
            "event_type": pa.Column(pa.String, pa.Check.isin(["VOICE", "MMS", "SMS", "DATA"])),
            "rate_plan_id": pa.Column(pa.Int, pa.Check.greater_than(-1)),
            "billing_flag_1": pa.Column(pa.Int, [pa.Check.greater_than(-1)]),
            "billing_flag_2": pa.Column(pa.Int, [pa.Check.greater_than(-1)]),
            "duration": pa.Column(pa.Int, [pa.Check.greater_than(-1)]),
            "charge": pa.Column(pa.Float, [pa.Check.greater_than(-1)]),
            "month": pa.Column(pa.String)
        },
        strict=True
        )
        self._data = self.in_connector.open()
        
        self._data = self._data.head(50000)
        self.additional_test()
        try:
            schema.validate(self._data, lazy=True)
            if self._LOG:
                self._LOG.info("Data Validated successfully. All looks good")
        

        except pa.errors.SchemaErrors as err:
            if self._LOG:
                self.LOG.info(err)
                self.LOG.info("Schema errors and failure cases:")
                self.LOG.info(err.failure_cases.head())
                self.LOG.info(f"Saving broken Checks at {DataCheck._FAILURE_CASES_DF_FILE}")
            err.failure_cases.to_csv("data/failure_cases.csv")
            if self._LOG:
                self.LOG.info("Please check if data is acceptable before loading it to db")



    def test_for_duplicates(self):
        duplicate_count = self._data.duplicated().sum()
        if duplicate_count != 0:
            if self._LOG:
                self.LOG.warning(f"Duplicated entries in Dataframe! Count: {duplicate_count}  percentage: {(duplicate_count/self._data.shape[0] * 100):.2f}%")
            if self._drop_duplicates:
                if self._LOG:
                    self.LOG.warning("Droping duplicates...")
                self._data.drop_duplicates(inplace=True)
            else:
                if self._LOG:
                    self.LOG.warning("Keeping duplicates within data!")
        if self._LOG:
            self.LOG.warning("Saving data")
        self._data.to_csv("data/pv_usage.csv", index=False)

    def test_datetime_column(self):
        if self._LOG:
            self.LOG.info("Trying to convert 'event_start_time' to datetime object")
        try:
            pd.to_datetime(self._data["event_start_time"], format='%Y-%m-%dT%H:%M:%S.%f%z')
        except Exception as e:
            if self._LOG:
                self.LOG.error("Could not convert 'event_start_time' to datetime object please check the column. Aborting...")
                self.LOG.error(e)
            raise e

    def additional_test(self):
        self.test_for_duplicates()
        self.test_datetime_column()