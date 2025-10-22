#!/usr/bin/env python3
"""
Test script to verify the FastAPI app imports correctly
"""

import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(__file__))

try:
    from app.main import app
    print("[SUCCESS] FastAPI app imports successfully")
    print(f"App title: {app.title}")
    print(f"App version: {app.version}")
except Exception as e:
    print(f"[ERROR] Failed to import FastAPI app: {e}")
    sys.exit(1)
