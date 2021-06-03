import pandas as pd
import pandera as pa

from pandera import Check, Column, DataFrameSchema

schema = pa.DataFrameSchema(
    columns={
        "int_column": Column(pa.Int),
        "float_column": Column(pa.Float, Check.greater_than(0)),
        "str_column": Column(pa.String, Check.isin(["a"])),
        "event_type": pa.Column(pa.String, pa.Check.isin(["DATA", "VOICE1", "SMS", "MMS"])),
        "date_column": Column(pa.DateTime),
    },
    strict=True
)

df = pd.DataFrame({
    "int_column": ["a", "b", "c"],
    "float_column": [0, 1, 2],
    "str_column": ["a", "b", "d"],
    "unknown_column": None,
})

schema.validate(df, lazy=True)