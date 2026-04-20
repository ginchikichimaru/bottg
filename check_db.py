from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db, Reminder, ReminderResponse , SessionLocal, ReminderCreate
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import Annotated

session_dep = Annotated[AsyncSession, Depends(SessionLocal)]

app = FastAPI(title="Станция подглядываний")
    
@app.get("/reminders/", response_model=List[ReminderResponse])
def get_reminders(db: Session = Depends(get_db)): 
    reminders = db.query(Reminder).all()
    return reminders

@app.post("/reminders/Trolling", response_model=List[ReminderResponse])
async def fill_remind(data: ReminderCreate, session: session_dep):
  user=data.user_id
  text=data.text
  


@app.get("/tables/")
def get_tables(db: Session = Depends(get_db)):
    from sqlalchemy import text
    result = db.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public';"))
    tables = [row[0] for row in result]
    return {"tables": tables}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)