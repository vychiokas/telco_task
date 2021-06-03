from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from pipeline.model.data_model import Base

_DB_NAME = "telco"
_CONNECTION_STRING = "postgresql+psycopg2://{0}:{1}@{2}/%s" % _DB_NAME
_DATABASE_IP = "172.18.0.1"
_DATABASE_PORT = "5432"
_USER_NAME = "postgres"
_PASSWORD = "example"

class DatabaseManager:
    __instance = None

    def __new__(cls):
        if DatabaseManager.__instance is None:
            DatabaseManager.__instance = object.__new__(cls)
            DatabaseManager.__instance.engine = create_engine(_CONNECTION_STRING.format(_USER_NAME, _PASSWORD, _DATABASE_IP+":"+_DATABASE_PORT), echo=False)
            
            # Create a configured "Session" class
            sm = sessionmaker(bind=DatabaseManager.__instance.engine, autoflush=True, autocommit=False)
            DatabaseManager.__instance.session = sm()
        return DatabaseManager.__instance

    def __getattr__(self, name):
        return getattr(self.__instance, name)

    def create_structure(self):
        Base.metadata.create_all(self.engine)

    def drop_structure(self):
        Base.metadata.drop_all(self.engine)

    def execute(self, statement):
        with self.engine.connect() as cn:
            cn.execute(statement)
    
    def recreate_table(self):
        self.dm.drop_structure()
        self.dm.create_structure()
         