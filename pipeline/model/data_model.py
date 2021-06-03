from sqlalchemy import Table, Column, Integer, ForeignKey, String, Float, DateTime
from sqlalchemy.orm import relationship, Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Serializer():
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Usage(Base, Serializer):
    __tablename__ = 'usage'
    customer_id = Column(Integer, primary_key=True)
    event_start_time = Column(DateTime)
    event_type = Column(String)
    rate_plan_id = Column(Integer)
    billing_flag_1 = Column(Integer)
    billing_flag_2 = Column(Integer)
    duration = Column(Integer)
    charge = Column(Float)
    month = Column(String)
    timestamp = Column(DateTime)


# class AggregatedEventType(Base, Serializer):
#     __tablename__ = 'event_type_aggregated'
#     event_type = Column(String)
#     timestamp = Column(DateTime)

# class AggregatedRatePlan(Base, Serializer):
#     __tablename__ = 'rate_plan_id_aggregated'
#     rate_plan_id = Column(Integer)
#     timestamp = Column(DateTime)