from .controller.db_manager import DatabaseManager, _DB_NAME
import pandas as pd
from sqlalchemy import inspect


class DatabaseImporter():
    def __init__(self, db_manager:DatabaseManager):
        self.dm = db_manager


    def run(self, dataframe:pd.DataFrame, table_name):
        inspector = inspect(self.dm.engine)
        if not inspector.has_table(table_name):
            self.dm.create_structure()

        dataframe.to_sql(
        table_name,
        self.dm.engine,
        if_exists='append',
        index=False,
        chunksize=5000,
)   
