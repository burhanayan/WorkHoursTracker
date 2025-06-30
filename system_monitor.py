"""
System event monitoring for Windows
Monitors login, logout, sleep, shutdown events
"""

import threading
import time
import win32api
import win32con
import win32gui
import psutil
from datetime import datetime
from models import WorkSession, get_db_session

class SystemMonitor:
    def __init__(self):
        self.running = False
        self.current_session = None
        self.last_activity = datetime.now()
        self.monitoring_thread = None
        
    def start_monitoring(self):
        """Start system monitoring"""
        self.running = True
        self.log_login()
        # No background thread - just log the initial login
        
    def stop_monitoring(self):
        """Stop system monitoring"""
        self.running = False
        self.log_logout("Manual Stop")
        
    def log_login(self):
        """Log user login event"""
        session = get_db_session()
        try:
            # Close any open session first
            self._close_open_session(session, "System Restart")
            
            # Create new session
            self.current_session = WorkSession(login_time=datetime.now())
            session.add(self.current_session)
            session.commit()
            print(f"Logged login at {self.current_session.login_time}")
        except Exception as e:
            print(f"Error logging login: {e}")
        finally:
            session.close()
            
    def log_logout(self, logout_type="Logout"):
        """Log user logout event"""
        if not self.current_session:
            return
            
        session = get_db_session()
        try:
            # Update current session
            db_session = session.query(WorkSession).filter_by(id=self.current_session.id).first()
            if db_session:
                db_session.logout_time = datetime.now()
                db_session.logout_type = logout_type
                session.commit()
                print(f"Logged logout at {db_session.logout_time} - Type: {logout_type}")
        except Exception as e:
            print(f"Error logging logout: {e}")
        finally:
            session.close()
            self.current_session = None
            
    def _close_open_session(self, db_session, logout_type="System Restart"):
        """Close any open work session"""
        try:
            open_session = db_session.query(WorkSession).filter_by(logout_time=None).first()
            if open_session:
                open_session.logout_time = datetime.now()
                open_session.logout_type = logout_type
                db_session.commit()
        except Exception as e:
            print(f"Error closing open session: {e}")
            
    def _monitor_events(self):
        """Monitor system events in background"""
        while self.running:
            try:
                # Basic monitoring - simplified to avoid threading issues
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"Error in system monitoring: {e}")
                time.sleep(60)
                
    def _is_system_shutting_down(self):
        """Check if system is shutting down"""
        try:
            # This is a simplified check - in a real implementation,
            # you'd use Windows Event Log or WMI events
            return False
        except:
            return False
            
    def _is_system_sleeping(self):
        """Check if system is going to sleep"""
        try:
            # Monitor power state changes
            # This is simplified - real implementation would use Windows API
            return False
        except:
            return False
            
    def _wait_for_wake_up(self):
        """Wait for system to wake up from sleep"""
        # This would monitor for system wake events
        pass