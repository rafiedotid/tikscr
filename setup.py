#!/usr/bin/env python3
"""
Setup script for TokCount Scraper
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def check_chrome():
    """Check if Chrome is installed"""
    print("Checking for Chrome installation...")
    # This is a basic check - Chrome path varies by system
    chrome_paths = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print("✅ Chrome found!")
            return True
    
    print("⚠️  Chrome not found in common locations. Please ensure Chrome is installed.")
    return False

def main():
    print("=== TokCount Scraper Setup ===")
    
    # Install requirements
    if not install_requirements():
        return
    
    # Check Chrome
    check_chrome()
    
    print("\n=== Setup Complete ===")
    print("You can now run the scraper with:")
    print("python tokcount_scraper_auto.py")
    print("\nOr customize the username in the script and run it.")

if __name__ == "__main__":
    main()