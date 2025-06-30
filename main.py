"""
Work Hours Tracker - System Tray Application
Main entry point for the application
"""

import sys
import threading
from work_tracker import WorkTracker

def main():
    """Main application entry point"""
    tracker = WorkTracker()
    
    # Start system monitoring in a separate thread
    monitor_thread = threading.Thread(target=tracker.start_monitoring, daemon=True)
    monitor_thread.start()
    
    # Start the system tray
    tracker.start_tray()

if __name__ == "__main__":
    main()