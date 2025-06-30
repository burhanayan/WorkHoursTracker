"""
Main Work Tracker class that combines system monitoring and tray functionality
"""

import pystray
from PIL import Image, ImageDraw
import threading
from datetime import datetime, timedelta
from system_monitor import SystemMonitor
from statistics_gui import StatisticsGUI
from settings_gui import SettingsGUI
from database_operations import DatabaseOperations

class WorkTracker:
    def __init__(self):
        self.system_monitor = SystemMonitor()
        self.db_ops = DatabaseOperations()
        self.tray_icon = None
        self.stats_gui = None
        self.settings_gui = None
        
    def create_tray_icon(self):
        """Create system tray icon"""
        # Create a simple icon
        image = Image.new('RGB', (32, 32), color='blue')
        draw = ImageDraw.Draw(image)
        draw.rectangle([8, 8, 24, 24], fill='white')
        draw.text((12, 12), "W", fill='blue')
        
        return image
        
    def get_tray_tooltip(self):
        """Get tooltip text for tray icon"""
        try:
            daily_hours = self.db_ops.get_daily_total_hours()
            last_login = self.db_ops.get_last_login_time()
            
            tooltip = f"Daily Hours: {daily_hours}"
            if last_login:
                if last_login.date() == datetime.now().date():
                    tooltip += f"\nLast Login: {last_login.strftime('%H:%M')}"
                else:
                    tooltip += f"\nLast Login: {last_login.strftime('%m/%d %H:%M')}"
                    
            return tooltip
        except Exception as e:
            return "Work Hours Tracker"
            
    def show_statistics(self, icon, item):
        """Show statistics window"""
        if self.stats_gui is None or not self.stats_gui.window.winfo_exists():
            self.stats_gui = StatisticsGUI()
        self.stats_gui.show()
        
    def show_settings(self, icon, item):
        """Show settings window"""
        if self.settings_gui is None or not self.settings_gui.window.winfo_exists():
            self.settings_gui = SettingsGUI()
        self.settings_gui.show()
        
    def quit_application(self, icon, item):
        """Quit the application"""
        self.system_monitor.stop_monitoring()
        icon.stop()
        
    def start_tray(self):
        """Start the system tray application"""
        # Create tray menu
        menu = pystray.Menu(
            pystray.MenuItem("Statistics", self.show_statistics),
            pystray.MenuItem("Settings", self.show_settings),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.quit_application)
        )
        
        # Create tray icon
        self.tray_icon = pystray.Icon(
            "WorkHoursTracker",
            self.create_tray_icon(),
            "Work Hours Tracker",
            menu
        )
        
        # Update tooltip periodically
        def update_tooltip():
            while True:
                try:
                    if self.tray_icon and self.tray_icon.visible:
                        self.tray_icon.title = self.get_tray_tooltip()
                    threading.Event().wait(60)  # Update every minute
                except:
                    break
                    
        tooltip_thread = threading.Thread(target=update_tooltip, daemon=True)
        tooltip_thread.start()
        
        # Run the tray icon
        self.tray_icon.run()
        
    def start_monitoring(self):
        """Start system monitoring"""
        self.system_monitor.start_monitoring()