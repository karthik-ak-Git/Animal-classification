#!/usr/bin/env python3
"""
Test script to verify deployment configuration
Run this locally before deploying to Render
"""

import os
import sys
from pathlib import Path

def test_files_exist():
    """Test if all required files exist"""
    print("🔍 Checking required files...")
    
    required_files = [
        "main_api.py",
        "start.py", 
        "requirements.txt",
        "render.yaml",
        "model.py",
        "data/dataloader.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files found")
        return True

def test_file_contents():
    """Test if key files have the right content"""
    print("🔍 Checking file contents...")
    
    try:
        # Check if main_api.py has health endpoint
        with open("main_api.py", "r", encoding="utf-8") as f:
            content = f.read()
            if "/health" in content and "health_check" in content:
                print("✅ Health endpoint found in main_api.py")
            else:
                print("❌ Health endpoint not found in main_api.py")
                return False
        
        # Check if start.py has proper configuration
        with open("start.py", "r", encoding="utf-8") as f:
            content = f.read()
            if "0.0.0.0" in content and "workers=1" in content:
                print("✅ Startup script properly configured")
            else:
                print("❌ Startup script not properly configured")
                return False
        
        # Check if render.yaml has health check
        with open("render.yaml", "r", encoding="utf-8") as f:
            content = f.read()
            if "healthCheckPath" in content and "/health" in content:
                print("✅ Render configuration has health check")
            else:
                print("❌ Render configuration missing health check")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ File content check failed: {e}")
        return False

def test_python_syntax():
    """Test if Python files have valid syntax"""
    print("🔍 Checking Python syntax...")
    
    python_files = ["main_api.py", "start.py", "model.py"]
    
    for file_path in python_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                compile(f.read(), file_path, "exec")
            print(f"✅ {file_path} has valid syntax")
        except SyntaxError as e:
            print(f"❌ {file_path} has syntax error: {e}")
            return False
        except Exception as e:
            print(f"⚠️  Could not check {file_path}: {e}")
    
    return True

def test_requirements_format():
    """Test if requirements.txt is properly formatted"""
    print("🔍 Checking requirements.txt format...")
    
    try:
        with open("requirements.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        if len(lines) > 0:
            print(f"✅ requirements.txt has {len(lines)} lines")
            return True
        else:
            print("❌ requirements.txt is empty")
            return False
            
    except Exception as e:
        print(f"❌ Could not read requirements.txt: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Animal Classification deployment configuration...")
    print("=" * 60)
    
    tests = [
        ("File existence", test_files_exist),
        ("File contents", test_file_contents),
        ("Python syntax", test_python_syntax),
        ("Requirements format", test_requirements_format)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Deployment configuration is ready.")
        print("\n📋 Next steps:")
        print("   1. Commit and push your changes to GitHub")
        print("   2. Connect your repository to Render")
        print("   3. Deploy using the render.yaml configuration")
        print("   4. Monitor deployment logs")
        print("   5. Test the /health endpoint once deployed")
    else:
        print("⚠️  Some tests failed. Please fix the issues before deploying.")
        print("\n🔧 Common fixes:")
        print("   - Check file paths and permissions")
        print("   - Verify Python syntax in all .py files")
        print("   - Ensure render.yaml has correct configuration")
    
    print("\n💡 Note: Dependencies will be installed during Render build")
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
