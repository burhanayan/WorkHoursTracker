"""
Database operations for Work Hours Tracker
"""

from datetime import datetime, timedelta
from sqlalchemy import func, and_
from models import WorkSession, Settings, get_db_session

class DatabaseOperations:
    def __init__(self):
        pass
        
    def get_daily_sessions(self, date=None):
        """Get work sessions for a specific day"""
        if date is None:
            date = datetime.now().date()
            
        session = get_db_session()
        try:
            sessions = session.query(WorkSession).filter(
                func.date(WorkSession.login_time) == date
            ).order_by(WorkSession.login_time).all()
            return sessions
        finally:
            session.close()
            
    def get_weekly_sessions(self, week_start=None):
        """Get work sessions for a specific week"""
        if week_start is None:
            today = datetime.now().date()
            week_start_day = self.get_week_start_day()
            days_since_start = (today.weekday() - week_start_day) % 7
            week_start = today - timedelta(days=days_since_start)
            
        week_end = week_start + timedelta(days=6)
        
        session = get_db_session()
        try:
            sessions = session.query(WorkSession).filter(
                and_(
                    func.date(WorkSession.login_time) >= week_start,
                    func.date(WorkSession.login_time) <= week_end
                )
            ).order_by(WorkSession.login_time).all()
            return sessions
        finally:
            session.close()
            
    def get_monthly_sessions(self, year=None, month=None):
        """Get work sessions for a specific month"""
        if year is None or month is None:
            today = datetime.now()
            year = today.year
            month = today.month
            
        session = get_db_session()
        try:
            sessions = session.query(WorkSession).filter(
                and_(
                    func.extract('year', WorkSession.login_time) == year,
                    func.extract('month', WorkSession.login_time) == month
                )
            ).order_by(WorkSession.login_time).all()
            return sessions
        finally:
            session.close()
            
    def get_yearly_sessions(self, year=None):
        """Get work sessions for a specific year"""
        if year is None:
            year = datetime.now().year
            
        session = get_db_session()
        try:
            sessions = session.query(WorkSession).filter(
                func.extract('year', WorkSession.login_time) == year
            ).order_by(WorkSession.login_time).all()
            return sessions
        finally:
            session.close()
            
    def calculate_session_duration(self, session):
        """Calculate duration of a work session"""
        if not session.logout_time:
            return timedelta(0)
        return session.logout_time - session.login_time
        
    def calculate_total_duration(self, sessions):
        """Calculate total duration from a list of sessions"""
        total = timedelta(0)
        for session in sessions:
            duration = self.calculate_session_duration(session)
            total += duration
        return total
        
    def format_duration(self, duration):
        """Format duration as 'Xhr Ymin'"""
        if isinstance(duration, timedelta):
            total_seconds = int(duration.total_seconds())
        else:
            total_seconds = 0
            
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}hr {minutes}min"
        else:
            return f"{minutes}min"
            
    def get_daily_total_hours(self, date=None):
        """Get formatted total hours for a day"""
        sessions = self.get_daily_sessions(date)
        total_duration = self.calculate_total_duration(sessions)
        return self.format_duration(total_duration)
        
    def get_weekly_total_hours(self, week_start=None):
        """Get formatted total hours for a week"""
        sessions = self.get_weekly_sessions(week_start)
        total_duration = self.calculate_total_duration(sessions)
        return self.format_duration(total_duration)
        
    def get_monthly_total_hours(self, year=None, month=None):
        """Get formatted total hours for a month"""
        sessions = self.get_monthly_sessions(year, month)
        total_duration = self.calculate_total_duration(sessions)
        return self.format_duration(total_duration)
        
    def get_yearly_total_hours(self, year=None):
        """Get formatted total hours for a year"""
        sessions = self.get_yearly_sessions(year)
        total_duration = self.calculate_total_duration(sessions)
        return self.format_duration(total_duration)
        
    def get_last_login_time(self):
        """Get the last login time"""
        session = get_db_session()
        try:
            last_session = session.query(WorkSession).order_by(WorkSession.login_time.desc()).first()
            return last_session.login_time if last_session else None
        finally:
            session.close()
            
    def get_week_start_day(self):
        """Get week start day setting (0=Monday, 6=Sunday)"""
        session = get_db_session()
        try:
            setting = session.query(Settings).filter_by(key='week_start_day').first()
            return int(setting.value) if setting else 0
        finally:
            session.close()
            
    def set_week_start_day(self, day):
        """Set week start day setting"""
        session = get_db_session()
        try:
            setting = session.query(Settings).filter_by(key='week_start_day').first()
            if setting:
                setting.value = str(day)
            else:
                setting = Settings(key='week_start_day', value=str(day))
                session.add(setting)
            session.commit()
        finally:
            session.close()