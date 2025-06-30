"""
Simple Work Hours Tracker - Minimal Version
"""

import tkinter as tk
from tkinter import ttk
import threading
from datetime import datetime
from database_operations import DatabaseOperations
from system_monitor import SystemMonitor

class SimpleTracker:
    def __init__(self):
        self.db_ops = DatabaseOperations()
        self.monitor = SystemMonitor()
        self.root = None
        
    def create_gui(self):
        """Create a simple GUI instead of system tray"""
        self.root = tk.Tk()
        self.root.title("Work Hours Tracker")
        self.root.geometry("300x200")
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Session Active", font=("Arial", 12, "bold"))
        self.status_label.pack(pady=10)
        
        # Buttons
        ttk.Button(main_frame, text="View Statistics", command=self.show_statistics).pack(pady=5, fill=tk.X)
        ttk.Button(main_frame, text="Manual Logout", command=self.manual_logout).pack(pady=5, fill=tk.X)
        ttk.Button(main_frame, text="Quit", command=self.quit_app).pack(pady=5, fill=tk.X)
        
        # Start monitoring
        self.monitor.start_monitoring()
        
        # Start GUI
        self.root.mainloop()
        
    def show_statistics(self):
        """Show statistics in a new window"""
        from statistics_gui import StatisticsGUI
        stats = StatisticsGUI()
        stats.show()
        
    def manual_logout(self):
        """Manual logout"""
        self.monitor.log_logout("Manual Logout")
        self.status_label.config(text="Session Ended - Click Quit to Exit")
        
    def quit_app(self):
        """Quit application"""
        self.monitor.stop_monitoring()
        self.root.quit()
        self.root.destroy()

def main():
    tracker = SimpleTracker()
    tracker.create_gui()

if __name__ == "__main__":
    main()