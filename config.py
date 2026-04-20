from aiogram import Router
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, create_engine
from sqlalchemy.ext.declarative import declarative_base
import datetime
Base = declarative_base()
engine = create_engine('postgresql://user:password@localhost/dbname')



router = Router()