from pipeline.data_check import DataCheck
from pipeline.data_source import CsvInputConnector
from utils.logger import LOG
import argparse
from pipeline.data_load import DatabaseImporter
from pipeline.controller.db_manager import DatabaseManager
import pandas as pd
from pipeline.cleaner import Cleaner
from pipeline.aggregation import Aggregator
from datetime import date

_DATA_FILE_PATH = "data/usage.csv"
_DATA_FILE_PATH_VALIDATED = "data/pv_usage.csv"
_NAMES=["customer_id", "event_start_time", "event_type", "rate_plan_id", "billing_flag_1", "billing_flag_2", "duration", "charge", "month"]

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-dv', "--datavalidation", help='Validation of incoming data',
                    action="store_true")
parser.add_argument('-a', "--aggregation", help='Aggregate data for the product people',
                action="store_true")
parser.add_argument('-p', "--populate", help='Populating data to the database of choice',
                action="store_true")
parser.add_argument('-e', "--erasedb", help='Delete and recreate Database',
                action="store_true")
parser.add_argument('-c', "--cleandb", help='Clean old entries',
                action="store_true")
args = parser.parse_args()


if args.erasedb:
    DatabaseManager().drop_structure()
    DatabaseManager().create_structure()

if args.datavalidation:
    input_connector = CsvInputConnector(_DATA_FILE_PATH, _NAMES)
    data_check = DataCheck(input_connector, log=LOG)
    data_check.run()

if args.populate:
    dataframe = CsvInputConnector(_DATA_FILE_PATH_VALIDATED).open()
    dataframe["timestamp"] = pd.to_datetime("now")
    # date.today().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    dataframe["event_start_time"] = pd.to_datetime(dataframe["event_start_time"], format='%Y-%m-%dT%H:%M:%S.%f%z')

    DatabaseImporter(DatabaseManager()).run(dataframe, "usage")

# TODO: Does not work yet needs fixing of the data model in order to automatically create a table within database and upload
if args.aggregation:
    input_connector = CsvInputConnector(_DATA_FILE_PATH_VALIDATED, _NAMES)
    
    agg = Aggregator(input_connector.open())
    input_connector = CsvInputConnector(_DATA_FILE_PATH)
    df = agg.aggregate("event_type")
    DatabaseImporter(DatabaseManager()).run(df, "aggreagation1")
    df = agg.aggregate("rate_plan_id")
    DatabaseImporter(DatabaseManager()).run(df, "aggreagation2")

if args.cleandb:
    Cleaner.delete_old_entries(DatabaseManager)