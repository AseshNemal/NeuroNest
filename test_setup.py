#!/usr/bin/env python3
"""
Quick test script to verify MindGarden components work correctly
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import pygame
        import PIL
        print("✅ All dependencies imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_assets():
    """Test if all required assets exist"""
    required_files = [
        "tree_small.png",
        "tree_medium.png", 
        "tree_large.png",
        "calm.mp3",
        "water.wav"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing asset files: {missing_files}")
        return False
    else:
        print("✅ All required asset files found")
        return True

def test_frames():
    """Test if frame files exist"""
    frames_dir = "frames"
    if not os.path.exists(frames_dir):
        print("❌ Frames directory not found")
        return False
    
    frame_files = [f for f in os.listdir(frames_dir) if f.startswith("frame_") and f.endswith(".png")]
    if len(frame_files) < 90:  # Should have close to 99 frames
        print(f"⚠️  Only {len(frame_files)} frame files found (expected ~99)")
        return False
    else:
        print(f"✅ Found {len(frame_files)} frame files")
        return True

def main():
    print("🧪 Testing NeuroNest MindGarden Project")
    print("=" * 40)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test assets
    if not test_assets():
        all_tests_passed = False
    
    # Test frames
    if not test_frames():
        all_tests_passed = False
    
    print("=" * 40)
    if all_tests_passed:
        print("🎉 All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("python mindgarden.py")
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
