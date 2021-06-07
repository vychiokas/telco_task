from sqlalchemy import Table, Column, Integer, String, Float, DateTime, MetaData



Meta = MetaData()

class Serializer():
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


usage = Table(
   'usage', Meta, 
   Column('id', Integer, primary_key=True, autoincrement=True),
   Column('customer_id', Integer), 
   Column('event_start_time', DateTime), 
   Column('event_type', String), 
   Column('rate_plan_id', Integer), 
   Column('billing_flag_1', Integer), 
   Column('billing_flag_2', Integer), 
   Column('duration', Integer), 
   Column('charge', Float), 
   Column('month', String), 
   Column('timestamp', DateTime)
)

aggregation1 = Table(
   'aggreagation1', Meta, 
   Column('id', Integer, primary_key = True, autoincrement=True), 
   Column('event_type', String), 
   Column('counts', Integer), 
   Column('timestamp', DateTime)
)

aggregation2 = Table(
   'aggreagation2', Meta, 
   Column('id', Integer, primary_key = True, autoincrement=True), 
   Column('rate_plan_id', String), 
   Column('counts', Integer), 
   Column('timestamp', DateTime)
)
