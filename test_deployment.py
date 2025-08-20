#!/usr/bin/env python3
"""
Test script for Vercel deployment setup
Run this to check if everything is configured correctly before deploying
"""

import os
import sys
from pathlib import Path


def check_file_exists(file_path, description):
    """Check if a file exists and print status"""
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"✅ {description}: {file_path} ({size:,} bytes)")
        return True
    else:
        print(f"❌ {description}: {file_path} (NOT FOUND)")
        return False


def check_vercel_setup():
    """Check if Vercel deployment files are properly configured"""
    print("🔍 Checking Vercel Deployment Setup...\n")

    # Check required files
    required_files = [
        ("vercel.json", "Vercel configuration"),
        ("requirements-vercel.txt", "Python dependencies"),
        ("api/index.py", "Main API entry point"),
        (".vercelignore", "Deployment ignore file"),
        ("outputs/best_model.pth", "Trained model"),
        ("frontend/index.html", "Frontend HTML"),
        ("frontend/styles.css", "Frontend CSS"),
        ("frontend/scripts.js", "Frontend JavaScript"),
    ]

    all_good = True
    for file_path, description in required_files:
        if not check_file_exists(file_path, description):
            all_good = False

    print("\n" + "="*50)

    # Check model size
    model_path = "outputs/best_model.pth"
    if os.path.exists(model_path):
        model_size_mb = os.path.getsize(model_path) / (1024 * 1024)
        if model_size_mb < 50:
            print(
                f"✅ Model size: {model_size_mb:.2f} MB (within Vercel 50MB limit)")
        else:
            print(
                f"⚠️ Model size: {model_size_mb:.2f} MB (exceeds Vercel 50MB limit)")
            all_good = False

    # Check Python modules
    print("\n🔍 Checking Python modules...")
    try:
        from utilss.species_fetcher import fetch_species_names
        print("✅ species_fetcher module")
    except ImportError:
        print("❌ species_fetcher module")
        all_good = False

    try:
        from utilss.dataset_manager import get_class_names_from_dataset
        print("✅ dataset_manager module")
    except ImportError:
        print("❌ dataset_manager module")
        all_good = False

    try:
        from model import AnimalCNN
        print("✅ model module")
    except ImportError:
        print("❌ model module")
        all_good = False

    try:
        from utilss.logger import log_correction
        print("✅ logger module")
    except ImportError:
        print("❌ logger module")
        all_good = False

    print("\n" + "="*50)

    if all_good:
        print("🎉 All checks passed! Ready for Vercel deployment.")
        print("\nNext steps:")
        print("1. Install Vercel CLI: npm install -g vercel")
        print("2. Login: vercel login")
        print("3. Deploy: vercel")
    else:
        print("❌ Some issues found. Please fix them before deploying.")

    return all_good


if __name__ == "__main__":
    check_vercel_setup()
