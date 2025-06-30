"""
Database models for Work Hours Tracker
"""

from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class WorkSession(Base):
    __tablename__ = 'work_sessions'
    
    id = Column(Integer, primary_key=True)
    login_time = Column(DateTime, nullable=False)
    logout_time = Column(DateTime, nullable=True)
    logout_type = Column(String(50), nullable=True)  # Sleep, Logout, Shutdown, etc.
    
    def __repr__(self):
        return f"<WorkSession(login={self.login_time}, logout={self.logout_time}, type={self.logout_type})>"

class Settings(Base):
    __tablename__ = 'settings'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(String(500), nullable=False)
    
    def __repr__(self):
        return f"<Settings(key={self.key}, value={self.value})>"

def get_db_session():
    """Get database session"""
    engine = create_engine('sqlite:///work_hours.db')
    Session = sessionmaker(bind=engine)
    return Session()