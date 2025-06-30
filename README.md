# Work Hours Tracker

A Windows system tray application that automatically tracks your work hours by monitoring login/logout, sleep, and shutdown events.

## Features

- **Automatic Tracking**: Monitors system events (login, logout, sleep, shutdown) automatically
- **System Tray Integration**: Runs quietly in the system tray with hover tooltip showing daily hours
- **Comprehensive Statistics**: View work hours by day, week, month, or year
- **Configurable Settings**: Customize week start day
- **Database Versioning**: Uses SQLite with Alembic for reliable data storage
- **Professional GUI**: Clean, tabbed interface for viewing statistics

## Screenshots

The application provides:
- System tray icon with hover tooltip showing daily worked hours
- Statistics window with 4 tabs: Daily, Weekly, Monthly, Yearly logs
- Settings page for configuring week start day
- Detailed work session logs with login/logout times and duration

## Installation

### Prerequisites
- Windows 10/11
- Python 3.7 or higher

### Setup Steps

1. **Clone or download** this repository to your desired location

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run setup script**:
   ```bash
   python setup.py
   ```

4. **Start the application**:
   ```bash
   python main.py
   ```
   
   Or double-click `start_tracker.bat`

## Usage

### System Tray
- The application runs in the system tray (bottom-right corner)
- **Hover** over the tray icon to see daily worked hours and last login time
- **Right-click** the tray icon to access the menu:
  - **Statistics**: Open the statistics window
  - **Settings**: Open settings to configure preferences
  - **Quit**: Exit the application

### Statistics Window
The statistics window contains four tabs:

#### Daily Logs
- Shows work sessions for a specific day
- Displays total daily worked hours
- Enter date in YYYY-MM-DD format

#### Weekly Logs
- Shows work sessions for a specific week
- Displays total weekly worked hours
- Week start day is configurable in settings

#### Monthly Logs
- Shows work sessions for a specific month
- Displays total monthly worked hours
- Enter year and month

#### Yearly Logs
- Shows work sessions for a specific year
- Displays total yearly worked hours

Each log shows:
- **Login Time**: When you logged in
- **Logout Time**: When you logged out (or "Active" if still logged in)
- **Logout Type**: How the session ended (Sleep, Logout, Shutdown, etc.)
- **Duration**: Total time worked in that session

### Settings
- **Week Start Day**: Configure which day starts your work week (Monday-Sunday)
- Settings are automatically saved to the database

## Database

The application uses SQLite database (`work_hours.db`) with Alembic for version management:
- **work_sessions**: Stores all login/logout events with timestamps
- **settings**: Stores application configuration

## File Structure

```
WorkHoursTracker/
├── main.py                 # Application entry point
├── work_tracker.py         # Main application class
├── system_monitor.py       # System event monitoring
├── statistics_gui.py       # Statistics window GUI
├── settings_gui.py         # Settings window GUI
├── database_operations.py  # Database query operations
├── models.py              # SQLAlchemy database models
├── requirements.txt       # Python dependencies
├── setup.py              # Setup and initialization script
├── alembic.ini           # Alembic configuration
├── alembic/              # Database migration files
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 001_initial_schema.py
├── work_hours.db         # SQLite database (created on first run)
└── start_tracker.bat     # Windows batch file for easy startup
```

## Automatic Startup (Optional)

To start the application automatically when Windows starts:

1. Press `Win + R`, type `shell:startup`, and press Enter
2. Copy `start_tracker.bat` to the Startup folder
3. The application will now start automatically when you log in

## Troubleshooting

### Application won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're running Python 3.7 or higher
- Run `python setup.py` to reinitialize the database

### System tray icon not visible
- Check your system tray settings in Windows
- Look for hidden icons in the system tray overflow area

### Database issues
- Delete `work_hours.db` and run `python setup.py` to recreate the database
- Check that the application has write permissions in its directory

### Statistics not updating
- Click the "Refresh" button in the statistics window
- Ensure the application is running and monitoring system events

## Technical Details

- **Framework**: Python with tkinter for GUI, pystray for system tray
- **Database**: SQLite with SQLAlchemy ORM and Alembic migrations
- **System Monitoring**: Windows API integration for event detection
- **Architecture**: Modular design with separate GUI, database, and monitoring components

## Contributing

This is a standalone application. For modifications:
1. Modify the relevant Python files
2. Update database schema in `alembic/versions/` if changing models
3. Test thoroughly on Windows systems
4. Update README.md with any new features or requirements

## License

This project is provided as-is for personal use. Modify and distribute as needed.