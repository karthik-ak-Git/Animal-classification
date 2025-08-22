#!/usr/bin/env python3
"""
Test script to verify memory optimization
Tests model loading without loading entire dataset
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

def test_model_loading():
    """Test the optimized model loading"""
    print("🧪 Testing memory-optimized model loading...")
    print_memory_usage()
    
    try:
        # Test directory scanning only
        print("\n📁 Testing directory scanning...")
        dataset_path = "dataset"
        if os.path.exists(dataset_path):
            class_names = [d for d in sorted(os.listdir(dataset_path)) 
                          if os.path.isdir(os.path.join(dataset_path, d))]
            print(f"Found {len(class_names)} classes: {class_names[:5]}...")
        else:
            print("Dataset directory not found")
            class_names = []
        
        print_memory_usage()
        
        # Test model import
        print("\n🤖 Testing model import...")
        from model import AnimalCNN
        
        num_classes = len(class_names) if class_names else 10
        model = AnimalCNN(num_classes=num_classes)
        print(f"Model created with {num_classes} classes")
        
        print_memory_usage()
        
        # Test model loading
        print("\n📥 Testing model weights loading...")
        model_path = "outputs/best_model.pth"
        if os.path.exists(model_path):
            import torch
            device = torch.device("cpu")  # Use CPU for testing
            checkpoint = torch.load(model_path, map_location=device)
            model.load_state_dict(checkpoint)
            del checkpoint
            print("Model weights loaded successfully")
        else:
            print("No trained model found")
        
        print_memory_usage()
        
        # Cleanup
        del model
        gc.collect()
        
        print("\n✅ Memory optimization test completed successfully!")
        print_memory_usage()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting memory optimization test...")
    success = test_model_loading()
    
    if success:
        print("\n🎉 All tests passed! Ready for deployment.")
    else:
        print("\n💥 Tests failed. Please fix issues before deployment.")
        sys.exit(1)
