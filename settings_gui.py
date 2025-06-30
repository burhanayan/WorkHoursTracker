"""
Settings GUI for Work Hours Tracker
Allows configuration of application settings
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database_operations import DatabaseOperations

class SettingsGUI:
    def __init__(self):
        self.db_ops = DatabaseOperations()
        self.window = None
        self.create_window()
        
    def create_window(self):
        """Create the settings window"""
        self.window = tk.Toplevel()
        self.window.title("Settings")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        # Main frame
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Week start day setting
        week_frame = ttk.LabelFrame(main_frame, text="Week Configuration", padding=10)
        week_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(week_frame, text="Start day of the week:").pack(anchor=tk.W)
        
        self.week_start_var = tk.StringVar()
        week_combo = ttk.Combobox(week_frame, textvariable=self.week_start_var, state="readonly", width=15)
        week_combo['values'] = (
            'Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday'
        )
        week_combo.pack(pady=5, anchor=tk.W)
        
        # Load current setting
        current_day = self.db_ops.get_week_start_day()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.week_start_var.set(days[current_day])
        
        # Database info
        db_frame = ttk.LabelFrame(main_frame, text="Database Information", padding=10)
        db_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(db_frame, text="Database file: work_hours.db").pack(anchor=tk.W)
        ttk.Label(db_frame, text="Using SQLite with Alembic versioning").pack(anchor=tk.W)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text="Save", command=self.save_settings).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(buttons_frame, text="Cancel", command=self.window.withdraw).pack(side=tk.RIGHT)
        
        # Hide window initially
        self.window.withdraw()
        
    def save_settings(self):
        """Save settings to database"""
        try:
            # Get selected day index
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            selected_day = self.week_start_var.get()
            day_index = days.index(selected_day)
            
            # Save to database
            self.db_ops.set_week_start_day(day_index)
            
            messagebox.showinfo("Settings", "Settings saved successfully!")
            self.window.withdraw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            
    def show(self):
        """Show the settings window"""
        # Refresh current settings
        current_day = self.db_ops.get_week_start_day()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.week_start_var.set(days[current_day])
        
        self.window.deiconify()
        self.window.lift()