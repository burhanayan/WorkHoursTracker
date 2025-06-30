"""
Statistics GUI for Work Hours Tracker
Displays daily, weekly, monthly, and yearly statistics
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from database_operations import DatabaseOperations

class StatisticsGUI:
    def __init__(self):
        self.db_ops = DatabaseOperations()
        self.window = None
        self.create_window()
        
    def create_window(self):
        """Create the statistics window"""
        self.window = tk.Toplevel()
        self.window.title("Work Hours Statistics")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_daily_tab()
        self.create_weekly_tab()
        self.create_monthly_tab()
        self.create_yearly_tab()
        
        # Refresh button
        refresh_btn = ttk.Button(self.window, text="Refresh", command=self.refresh_all_tabs)
        refresh_btn.pack(pady=5)
        
        # Hide window initially
        self.window.withdraw()
        
    def create_daily_tab(self):
        """Create daily statistics tab"""
        daily_frame = ttk.Frame(self.notebook)
        self.notebook.add(daily_frame, text="Daily Logs")
        
        # Date selection
        date_frame = ttk.Frame(daily_frame)
        date_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(date_frame, text="Date:").pack(side=tk.LEFT)
        self.daily_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.daily_date_entry = ttk.Entry(date_frame, textvariable=self.daily_date_var, width=12)
        self.daily_date_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(date_frame, text="Load", command=self.load_daily_data).pack(side=tk.LEFT, padx=5)
        
        # Total hours label
        self.daily_total_label = ttk.Label(daily_frame, text="Daily Worked: 0hr 0min", font=("Arial", 12, "bold"))
        self.daily_total_label.pack(pady=5)
        
        # Treeview for data
        self.daily_tree = self.create_treeview(daily_frame)
        
    def create_weekly_tab(self):
        """Create weekly statistics tab"""
        weekly_frame = ttk.Frame(self.notebook)
        self.notebook.add(weekly_frame, text="Weekly Logs")
        
        # Week selection
        week_frame = ttk.Frame(weekly_frame)
        week_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(week_frame, text="Week Start:").pack(side=tk.LEFT)
        
        # Calculate current week start
        today = datetime.now().date()
        week_start_day = self.db_ops.get_week_start_day()
        days_since_start = (today.weekday() - week_start_day) % 7
        current_week_start = today - timedelta(days=days_since_start)
        
        self.weekly_date_var = tk.StringVar(value=current_week_start.strftime("%Y-%m-%d"))
        self.weekly_date_entry = ttk.Entry(week_frame, textvariable=self.weekly_date_var, width=12)
        self.weekly_date_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(week_frame, text="Load", command=self.load_weekly_data).pack(side=tk.LEFT, padx=5)
        
        # Total hours label
        self.weekly_total_label = ttk.Label(weekly_frame, text="Weekly Worked: 0hr 0min", font=("Arial", 12, "bold"))
        self.weekly_total_label.pack(pady=5)
        
        # Treeview for data
        self.weekly_tree = self.create_treeview(weekly_frame)
        
    def create_monthly_tab(self):
        """Create monthly statistics tab"""
        monthly_frame = ttk.Frame(self.notebook)
        self.notebook.add(monthly_frame, text="Monthly Logs")
        
        # Month selection
        month_frame = ttk.Frame(monthly_frame)
        month_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(month_frame, text="Year:").pack(side=tk.LEFT)
        self.monthly_year_var = tk.StringVar(value=str(datetime.now().year))
        self.monthly_year_entry = ttk.Entry(month_frame, textvariable=self.monthly_year_var, width=6)
        self.monthly_year_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(month_frame, text="Month:").pack(side=tk.LEFT, padx=(10, 0))
        self.monthly_month_var = tk.StringVar(value=str(datetime.now().month))
        self.monthly_month_entry = ttk.Entry(month_frame, textvariable=self.monthly_month_var, width=4)
        self.monthly_month_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(month_frame, text="Load", command=self.load_monthly_data).pack(side=tk.LEFT, padx=5)
        
        # Total hours label
        self.monthly_total_label = ttk.Label(monthly_frame, text="Monthly Worked: 0hr 0min", font=("Arial", 12, "bold"))
        self.monthly_total_label.pack(pady=5)
        
        # Treeview for data
        self.monthly_tree = self.create_treeview(monthly_frame)
        
    def create_yearly_tab(self):
        """Create yearly statistics tab"""
        yearly_frame = ttk.Frame(self.notebook)
        self.notebook.add(yearly_frame, text="Yearly Logs")
        
        # Year selection
        year_frame = ttk.Frame(yearly_frame)
        year_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(year_frame, text="Year:").pack(side=tk.LEFT)
        self.yearly_year_var = tk.StringVar(value=str(datetime.now().year))
        self.yearly_year_entry = ttk.Entry(year_frame, textvariable=self.yearly_year_var, width=6)
        self.yearly_year_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(year_frame, text="Load", command=self.load_yearly_data).pack(side=tk.LEFT, padx=5)
        
        # Total hours label
        self.yearly_total_label = ttk.Label(yearly_frame, text="Yearly Worked: 0hr 0min", font=("Arial", 12, "bold"))
        self.yearly_total_label.pack(pady=5)
        
        # Treeview for data
        self.yearly_tree = self.create_treeview(yearly_frame)
        
    def create_treeview(self, parent):
        """Create a treeview widget for displaying data"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview
        columns = ("Login", "Logout", "Type", "Duration")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        tree.heading("Login", text="Login Time")
        tree.heading("Logout", text="Logout Time")
        tree.heading("Type", text="Logout Type")
        tree.heading("Duration", text="Duration")
        
        tree.column("Login", width=150)
        tree.column("Logout", width=150)
        tree.column("Type", width=100)
        tree.column("Duration", width=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        h_scrollbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack everything
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        return tree
        
    def populate_treeview(self, tree, sessions, total_label, total_hours):
        """Populate treeview with session data"""
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)
            
        # Add sessions
        for session in sessions:
            login_time = session.login_time.strftime("%Y-%m-%d %H:%M:%S")
            logout_time = session.logout_time.strftime("%Y-%m-%d %H:%M:%S") if session.logout_time else "Active"
            logout_type = session.logout_type or "N/A"
            duration = self.db_ops.format_duration(self.db_ops.calculate_session_duration(session))
            
            tree.insert("", tk.END, values=(login_time, logout_time, logout_type, duration))
            
        # Update total label
        total_label.config(text=f"{total_label.cget('text').split(':')[0]}: {total_hours}")
        
    def load_daily_data(self):
        """Load daily data"""
        try:
            date = datetime.strptime(self.daily_date_var.get(), "%Y-%m-%d").date()
            sessions = self.db_ops.get_daily_sessions(date)
            total_hours = self.db_ops.get_daily_total_hours(date)
            self.populate_treeview(self.daily_tree, sessions, self.daily_total_label, total_hours)
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            
    def load_weekly_data(self):
        """Load weekly data"""
        try:
            week_start = datetime.strptime(self.weekly_date_var.get(), "%Y-%m-%d").date()
            sessions = self.db_ops.get_weekly_sessions(week_start)
            total_hours = self.db_ops.get_weekly_total_hours(week_start)
            self.populate_treeview(self.weekly_tree, sessions, self.weekly_total_label, total_hours)
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            
    def load_monthly_data(self):
        """Load monthly data"""
        try:
            year = int(self.monthly_year_var.get())
            month = int(self.monthly_month_var.get())
            sessions = self.db_ops.get_monthly_sessions(year, month)
            total_hours = self.db_ops.get_monthly_total_hours(year, month)
            self.populate_treeview(self.monthly_tree, sessions, self.monthly_total_label, total_hours)
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid year or month")
            
    def load_yearly_data(self):
        """Load yearly data"""
        try:
            year = int(self.yearly_year_var.get())
            sessions = self.db_ops.get_yearly_sessions(year)
            total_hours = self.db_ops.get_yearly_total_hours(year)
            self.populate_treeview(self.yearly_tree, sessions, self.yearly_total_label, total_hours)
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid year")
            
    def refresh_all_tabs(self):
        """Refresh all tabs with current data"""
        self.load_daily_data()
        self.load_weekly_data()
        self.load_monthly_data()
        self.load_yearly_data()
        
    def show(self):
        """Show the statistics window"""
        self.window.deiconify()
        self.window.lift()
        self.refresh_all_tabs()