from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Reminder, ReminderResponse, SessionLocal, ReminderCreate, SecretMessage, SecretMessageResponse, User, Transaction, TransactionResponse, FinancialGoal, FinancialGoalResponse
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import Annotated
import os
from sqlalchemy import desc

from database import test_db_connection

ADMIN_ID = int(os.getenv("ADMIN_ID", "0")) 

app = FastAPI(title="Станция подглядываний")

@app.get("/health/db-connect")
def health_db_connect():
    return test_db_connection()

@app.get("/health/tables")
def health_tables(db: Session = Depends(get_db)):
    from sqlalchemy import text
    result = db.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public';"))
    tables = [row[0] for row in result.fetchall()]
    expected_tables = ['users', 'transactions', 'financial_goals', 'reminders', 'secret_messages']
    missing = [t for t in expected_tables if t not in tables]
    return {
        'status': 'ok' if not missing else 'warning',
        'tables_count': len(tables),
        'missing_tables': missing
    }
    
@app.get("/reminders/", response_model=List[ReminderResponse])
def get_reminders(db: Session = Depends(get_db)): 
    reminders = db.query(Reminder).all()
    return reminders

@app.post("/reminders/", response_model=ReminderResponse)
async def create_reminder(data: ReminderCreate, db: Session = Depends(get_db)):
    reminder = Reminder(**data.dict())
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder
  


@app.get("/users/", response_model=List)
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "user_id": user.user_id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": user.created_at
        }
        for user in users
    ]

@app.get("/secret_messages/", response_model=List[SecretMessageResponse])
def get_secret_messages(user_id: int, db: Session = Depends(get_db)):
    if user_id != ADMIN_ID:
        raise HTTPException(status_code=403, detail="Access denied")
    messages = db.query(SecretMessage).all()
    return messages

@app.get("/tables/")
def get_tables(db: Session = Depends(get_db)):
    from sqlalchemy import text
    result = db.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public';"))
    tables = [row[0] for row in result]
    return {"tables": tables}


@app.get("/transactions/{user_id}/", response_model=List[TransactionResponse])
def get_user_transactions(user_id: int, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).order_by(desc(Transaction.created_at)).all()
    return transactions


@app.get("/transactions/{user_id}/balance")
def get_user_balance(user_id: int, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    total_balance = sum(t.amount for t in transactions) if transactions else 0
    return {
        "user_id": user_id,
        "balance": total_balance,
        "transaction_count": len(transactions)
    }


@app.get("/goals/{user_id}/", response_model=List[FinancialGoalResponse])
def get_user_goals(user_id: int, db: Session = Depends(get_db)):
    goals = db.query(FinancialGoal).filter(FinancialGoal.user_id == user_id).all()
    return goals


@app.get("/goals/{user_id}/current", response_model=FinancialGoalResponse)
def get_current_goal(user_id: int, db: Session = Depends(get_db)):
    goal = db.query(FinancialGoal).filter(FinancialGoal.user_id == user_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)