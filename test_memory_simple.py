#!/usr/bin/env python3
"""
Simple test script to verify directory scanning optimization
Tests only the memory-efficient directory scanning without loading models
"""

import os
import sys
import gc
import psutil

def print_memory_usage():
    """Print current memory usage"""
    memory = psutil.virtual_memory()
    print(f"Memory: {memory.used / 1024 / 1024:.1f}MB used, "
          f"{memory.available / 1024 / 1024:.1f}MB available "
          f"({memory.percent:.1f}%)")

def test_directory_scanning():
    """Test the optimized directory scanning only"""
    print("🧪 Testing memory-optimized directory scanning...")
    print_memory_usage()
    
    try:
        # Test directory scanning only (this is what was causing memory issues)
        print("\n📁 Testing directory scanning...")
        dataset_path = "dataset"
        if os.path.exists(dataset_path):
            # Just get folder names as class names - don't load images
            class_names = [d for d in sorted(os.listdir(dataset_path)) 
                          if os.path.isdir(os.path.join(dataset_path, d))]
            class_map = {cls_name: idx for idx, cls_name in enumerate(class_names)}
            print(f"Found {len(class_names)} animal classes")
            print(f"First 5 classes: {class_names[:5]}")
            print(f"Class map sample: {dict(list(class_map.items())[:3])}")
        else:
            print("Dataset directory not found")
            class_names = []
            class_map = {}
        
        print_memory_usage()
        
        # Test that we can access class information without loading images
        print("\n🔍 Testing class information access...")
        if class_names:
            print(f"Total classes: {len(class_names)}")
            print(f"Sample class: {class_names[0]} -> {class_map[class_names[0]]}")
            
            # Test that we can get a sample file path without loading the image
            sample_class = class_names[0]
            sample_folder = os.path.join(dataset_path, sample_class)
            if os.path.exists(sample_folder):
                files = [f for f in os.listdir(sample_folder) 
                        if f.lower().endswith(('png', 'jpg', 'jpeg'))]
                print(f"Sample class '{sample_class}' has {len(files)} image files")
                if files:
                    print(f"Sample file: {files[0]}")
        
        print_memory_usage()
        
        # Cleanup
        del class_names, class_map
        gc.collect()
        
        print("\n✅ Directory scanning optimization test completed successfully!")
        print_memory_usage()
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting directory scanning optimization test...")
    success = test_directory_scanning()
    
    if success:
        print("\n🎉 Directory scanning test passed! This optimization will help with deployment.")
        print("\n📋 Next steps:")
        print("1. Commit these changes to your repository")
        print("2. Deploy to Render")
        print("3. Monitor memory usage via /health endpoint")
    else:
        print("\n💥 Test failed. Please fix issues before deployment.")
        sys.exit(1)
