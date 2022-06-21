from sqlalchemy import DATETIME, Column, ForeignKey, Integer, String,Boolean,TIME,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func
import sqlalchemy as db
import datetime
import os



# ---------------------------------------------
Base = declarative_base()

class gainers(Base):#if spare time left can add a emp id and link this with schedules already
    __tablename__ = 'GainersOfTheDay'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Date=Column(String(250))
    Symbol = Column(String(250), nullable=False)
    Name = Column(String(250), nullable=False)
    Price_Intraday = Column(Float, nullable=False)
    Change = Column(String(250),default=False, nullable=False)
    ChangeByPercentage = Column(String(10),default=False, nullable=False)
    Volume = Column(String(20),default=False, nullable=False)
    MarketCap = Column(String(20),default=False, nullable=False)
    Link=Column(String(250), nullable=False)
    
class mostactive(Base):#if spare time left can add a emp id and link this with schedules already
    __tablename__ = 'MostActiveOfTheDay'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Date=Column(String(250))
    Symbol = Column(String(250), nullable=False)
    Name = Column(String(250), nullable=False)
    Price_Intraday = Column(Float, nullable=False)
    Change = Column(Float,default=False, nullable=False)
    ChangeByPercentage = Column(String(10),default=False, nullable=False)
    Volume = Column(String(20),default=False, nullable=False)
    MarketCap = Column(String(20),default=False, nullable=False)
    Link=Column(String(250), nullable=False)

class trendingtickers(Base):#if spare time left can add a emp id and link this with schedules already
    __tablename__ = 'TrendingTickerOfTheDay'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Date=Column(String(250))
    Symbol = Column(String(250), nullable=False)
    Name = Column(String(250), nullable=False)
    Change = Column(String(250), nullable=False)
    Volume = Column(String(250),default=False, nullable=False)
    ChangeByPercentage = Column(String(10),default=False, nullable=False)
    MarketCap = Column(String(20),default=False, nullable=False)
    LastPrice = Column(String(20),default=False, nullable=False)
    Link=Column(String(250), nullable=False)


filename = os.path.abspath(__file__)
dbdir = filename.rstrip('Database_implementation.py')
dbpath = os.path.join(dbdir, "findatabase.db")
engine = create_engine(f'sqlite://///{dbpath}.sqlite3',echo=True) 
Base.metadata.create_all(engine)