from sqlalchemy import Column, Integer, String, DateTime, BigInteger, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import  async_sessionmaker, AsyncSession
import datetime
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Reminder(Base):
    __tablename__ = "reminders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    

class SecretMessage(Base):
    __tablename__ = "secret_messages"
    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(BigInteger, nullable=False)
    to_user_id = Column(BigInteger, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


Base.metadata.create_all(bind=engine)


class ReminderCreate(BaseModel):
    user_id: int
    text: str

class ReminderResponse(BaseModel):
    id: int
    user_id: int
    text: str
    created_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True

class SecretMessageCreate(BaseModel):
    to_user_id: int
    message: str

class SecretMessageResponse(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    message: str
    created_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()