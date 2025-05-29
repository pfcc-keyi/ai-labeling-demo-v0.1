from sqlmodel import SQLModel, Field, create_engine, Session
from datetime import datetime
from typing import Optional
import os

class RequestLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    account_id: str
    model_name: str
    input_text: str
    predicted_label: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    processing_time: Optional[float] = None
    error_message: Optional[str] = None

class FeedbackLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: int = Field(foreign_key="requestlog.id")
    account_id: str
    is_supported: bool
    corrected_label: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Database setup
DATABASE_URL = "sqlite:///./logs.db"
engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session 