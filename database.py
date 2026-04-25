from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Float, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
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
    message = Column(String, nullable=True)
    photo_file_id = Column(String, nullable=True)
    photo_caption = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False)
    amount = Column(Float, nullable=False)  # + для дохода, - для траты
    description = Column(String, nullable=True)
    transaction_type = Column(String, nullable=False)  # "income" или "expense"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class FinancialGoal(Base):
    __tablename__ = "financial_goals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False)
    goal_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


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


class TransactionCreate(BaseModel):
    amount: float
    description: Optional[str] = None
    transaction_type: str  # "income" или "expense"

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    description: Optional[str] = None
    transaction_type: str
    created_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True


class FinancialGoalCreate(BaseModel):
    goal_amount: float
    description: Optional[str] = None

class FinancialGoalResponse(BaseModel):
    id: int
    user_id: int
    goal_amount: float
    current_amount: float
    description: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

class SecretMessageCreate(BaseModel):
    to_user_id: int
    message: str

class SecretMessageResponse(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    message: Optional[str] = None
    photo_file_id: Optional[str] = None
    photo_caption: Optional[str] = None
    created_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_db_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {'status': 'ok', 'message': 'DB connected'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
