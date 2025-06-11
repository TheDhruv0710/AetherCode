"""
AetherCode - Startup Script
This script starts both the frontend and backend servers
"""

import os
import subprocess
import sys
import threading
import time
import webbrowser

def start_backend():
    """Start the Flask backend server"""
    print("Starting backend server...")
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
    
    # Check if we're on Windows or Unix
    if sys.platform.startswith('win'):
        process = subprocess.Popen(["python", "run_backend.py"], cwd=backend_dir)
    else:
        process = subprocess.Popen(["python3", "run_backend.py"], cwd=backend_dir)
    
    return process

def start_frontend():
    """Start the frontend server using Python's http.server"""
    print("Starting frontend server...")
    frontend_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if we're on Windows or Unix
    if sys.platform.startswith('win'):
        process = subprocess.Popen(["python", "-m", "http.server", "8000"], cwd=frontend_dir)
    else:
        process = subprocess.Popen(["python3", "-m", "http.server", "8000"], cwd=frontend_dir)
    
    return process

def main():
    """Main function to start both servers"""
    print("Starting AetherCode application...")
    
    # Start backend server in a separate process
    backend_process = start_backend()
    
    # Wait for backend to initialize
    print("Waiting for backend server to initialize...")
    time.sleep(2)
    
    # Start frontend server in a separate process
    frontend_process = start_frontend()
    
    # Wait for frontend to initialize
    print("Waiting for frontend server to initialize...")
    time.sleep(1)
    
    # Open the application in the default web browser
    print("Opening AetherCode in your web browser...")
    webbrowser.open("http://localhost:8000")
    
    print("\nAetherCode is now running!")
    print("Frontend: http://localhost:8000")
    print("Backend API: http://localhost:5000/api")
    print("\nPress Ctrl+C to stop the servers")
    
    try:
        # Keep the script running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down AetherCode...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Servers stopped. Goodbye!")

if __name__ == "__main__":
    main()
