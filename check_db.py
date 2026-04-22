from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Reminder, ReminderResponse , SessionLocal, ReminderCreate, SecretMessage, SecretMessageResponse, User
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import Annotated
import os

session_dep = Annotated[AsyncSession, Depends(SessionLocal)]

ADMIN_ID = int(os.getenv("ADMIN_ID", "0")) 

app = FastAPI(title="Станция подглядываний")
    
@app.get("/reminders/", response_model=List[ReminderResponse])
def get_reminders(db: Session = Depends(get_db)): 
    reminders = db.query(Reminder).all()
    return reminders

@app.post("/reminders/Trolling", response_model=List[ReminderResponse])
async def fill_remind(data: ReminderCreate, session: session_dep):
  user=data.user_id
  text=data.text
  


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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)