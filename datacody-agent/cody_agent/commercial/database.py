from sqlalchemy import create_engine, Column, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True)
    tier = Column(String, default="developer")
    stripe_id = Column(String)
    monthly_usage = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class UsageRecord(Base):
    __tablename__ = "usage_records"
    id = Column(String, primary_key=True)
    user_id = Column(String)
    cost = Column(Float)
    task_hash = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)

Base.metadata.create_all(bind=engine)
