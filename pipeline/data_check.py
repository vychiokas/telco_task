import pandas as pd
import pdb
import pandera as pa
from pandera import Check, Column


df = pd.read_csv("data/usage.csv", names=["customer_id", "event_start_time", "event_type", "rate_plan_id", "billing_flag_1", "billing_flag_2", "duration", "charge", "month"])

schema = pa.DataFrameSchema(
    columns={
        "customer_id": Column(pa.Int, [Check.greater_than(0)]),
        "event_start_time": Column(pa.String),
        "event_type": Column(pa.String, [Check.isin(["DATA", "VOICE", "SMS", "MMS"])]),
        "rate_plan_id": Column(pa.Int, [Check.greater_than(0)]),
        "billing_flag_1": Column(pa.Int, [Check.greater_than(0)]),
        "billing_flag_2": Column(pa.Int, [Check.greater_than(0)]),
        "duration": Column(pa.Int, [Check.greater_than(0)]),
        "charge": Column(pa.Float, [Check.greater_than(0)]),
        "month": Column(pa.String)
    },
    strict=True
)

try:
    print("I am trying")
    schema.validate(df, lazy=True)
except pa.errors.SchemaErrors as err:
    print("I am in except")
    print(err)
    print(dir(err))
    print(dir(err.data))
    print("Schema errors and failure cases:")
    print(err.failure_cases.head())
    print("\nDataFrame object that failed validation:")
    print(err.data.head())
    