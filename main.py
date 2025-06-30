"""
Work Hours Tracker - System Tray Application
Main entry point for the application
"""

import sys
from work_tracker import WorkTracker

def main():
    """Main application entry point"""
    tracker = WorkTracker()
    
    # Start system monitoring (no separate thread)
    tracker.start_monitoring()
    
    # Start the system tray
    tracker.start_tray()

if __name__ == "__main__":
    main()