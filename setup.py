"""
Setup script for Work Hours Tracker
"""

import sqlite3
import os
from alembic.config import Config
from alembic import command

def setup_database():
    """Initialize database with Alembic migrations"""
    print("Setting up database...")
    
    # Create alembic configuration
    alembic_cfg = Config("alembic.ini")
    
    # Run database migrations
    try:
        command.upgrade(alembic_cfg, "head")
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False
    
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("Checking dependencies...")
    
    required_packages = [
        'pystray', 'Pillow', 'psutil', 'sqlalchemy', 'alembic', 'pywin32'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').lower())
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    print("All dependencies are installed!")
    return True

def create_startup_script():
    """Create a batch file for easy startup"""
    script_content = '''@echo off
cd /d "%~dp0"
python main.py
pause
'''
    
    with open("start_tracker.bat", "w") as f:
        f.write(script_content)
    
    print("Created start_tracker.bat for easy startup")

def main():
    """Main setup function"""
    print("Work Hours Tracker Setup")
    print("=" * 30)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Setup database
    if not setup_database():
        return
    
    # Create startup script
    create_startup_script()
    
    print("\nSetup completed successfully!")
    print("\nTo start the application:")
    print("1. Run 'python main.py' or")
    print("2. Double-click 'start_tracker.bat'")
    print("\nThe application will run in the system tray.")

if __name__ == "__main__":
    main()