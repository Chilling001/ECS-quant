#!/usr/bin/env python3
"""
Quick start script for the Streamlit web dashboard.
Provides an easy way to launch the modern web interface.
"""
import subprocess
import sys
import os

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        print("✓ Streamlit is installed")
        return True
    except ImportError:
        print("✗ Streamlit is not installed")
        print("\nInstalling dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✓ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install dependencies")
            return False

def check_config():
    """Check if config file exists."""
    if os.path.exists('config.py'):
        print("✓ Configuration file found")
        return True
    else:
        print("⚠ Warning: config.py not found")
        print("  The bot will use environment variables or demo mode")
        print("  To configure: cp config_template.py config.py")
        return False

def main():
    """Main entry point."""
    print("=" * 60)
    print("AI Forex Trading Bot - Streamlit Web Dashboard")
    print("=" * 60)
    print()
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install dependencies manually:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    # Check config
    check_config()
    
    print()
    print("=" * 60)
    print("Starting Streamlit Web Dashboard...")
    print("=" * 60)
    print()
    print("The dashboard will open in your default browser.")
    print("If it doesn't, navigate to: http://localhost:8501")
    print()
    print("Press Ctrl+C to stop the server")
    print()
    
    # Launch streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        print("Dashboard stopped.")

if __name__ == "__main__":
    main()
