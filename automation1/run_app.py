#!/usr/bin/env python3
"""
Health AI Assistant - Application Runner

This script runs the Streamlit application with proper configuration.
Make sure all your original CrewAI files (agents.py, tasks2.py, tool2.py) 
are in the same directory as this runner.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit',
        'crewai',
        'schedule'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_original_files():
    """Check if original CrewAI files exist"""
    required_files = ['agents.py', 'tasks2.py', 'tool2.py']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"Missing required CrewAI files: {', '.join(missing_files)}")
        print("Please ensure your original CrewAI files are in the same directory.")
        return False
    
    return True

def create_docs_directory():
    docs_dir = Path('../docs')
    docs_dir.mkdir(exist_ok=True)
    
    # Create files with basic content
    files_content = {
        'profile.txt': "User medical profile and health information",
        'reportformat.txt': "Health report format template",
        'dr_records.txt': "Medical consultation records",
        'advic_records.txt': "Performance and wearable data records", 
        'carla_records.txt': "Nutrition consultation records",
        'rachel_records.txt': "Exercise and physiotherapy records",
        'ruby_records.txt': "Progress tracking and coordination records"
    }
    
    for filename, content in files_content.items():
        filepath = docs_dir / filename
        if not filepath.exists():
            filepath.write_text(f"# {content}\n\n")
def run_application():
    """Run the Streamlit application"""
    if not check_dependencies():
        return
    
    if not check_original_files():
        print("Warning: Some CrewAI files are missing. The app will run in fallback mode.")
    
    # Create necessary directories
    create_docs_directory()
    
    # Set environment variables for better Streamlit experience
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = 'localhost'
    
    print("Starting Health AI Assistant...")
    print("The application will open in your default web browser.")
    print("If it doesn't open automatically, visit: http://localhost:8501")
    print("\nPress Ctrl+C to stop the application.")
    
    try:
        # Run the Streamlit app
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'main.py',
            '--server.port=8501',
            '--server.address=localhost',
            '--browser.serverAddress=localhost'
        ])
    except KeyboardInterrupt:
        print("\nApplication stopped.")
    except Exception as e:
        print(f"Error running application: {e}")

if __name__ == "__main__":
    run_application()