#!/usr/bin/env python3
import subprocess
import sys
import os
import time

def install_requirements():
    print("Installing requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Downloading spaCy model...")
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])

def start_backend():
    print("Starting FastAPI backend...")
    return subprocess.Popen([sys.executable, "main.py"])

def start_frontend():
    print("Starting Streamlit frontend...")
    return subprocess.Popen([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])

if __name__ == "__main__":
    # Install dependencies if needed
    if "--install" in sys.argv:
        install_requirements()
    
    # Start backend
    backend_process = start_backend()
    time.sleep(3)  # Give backend time to start
    
    # Start frontend
    frontend_process = start_frontend()
    
    try:
        print("\n" + "="*50)
        print("🚀 DEMO IS RUNNING!")
        print("Backend: http://localhost:8000")
        print("Frontend: http://localhost:8501")
        print("="*50)
        print("Press Ctrl+C to stop both services")
        
        # Wait for processes
        backend_process.wait()
        frontend_process.wait()
        
    except KeyboardInterrupt:
        print("\nShutting down...")
        backend_process.terminate()
        frontend_process.terminate()