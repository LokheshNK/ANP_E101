#!/usr/bin/env python3
"""
Test script to verify data generation and processing works correctly
"""

import os
import sys
import json
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_data_generation():
    """Test the synthetic data generation"""
    print("🧪 Testing Data Generation...")
    
    try:
        from scripts.generate_synthetic_data import SyntheticDataGenerator
        
        # Generate data with fixed seed for reproducibility
        generator = SyntheticDataGenerator(seed=42)
        file_paths = generator.generate_all_data()
        
        print("✅ Data generation successful!")
        
        # Verify files exist and have content
        for data_type, path in file_paths.items():
            if os.path.exists(path):
                with open(path, 'r') as f:
                    data = json.load(f)
                print(f"  - {data_type}: {len(data)} records")
            else:
                print(f"  ❌ {data_type}: File not found at {path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_activity_calculation():
    """Test the activity-based metrics calculation"""
    print("\n🧪 Testing Activity Calculation...")
    
    try:
        from scripts.calculate_attendance_from_activity import get_activity_based_metrics
        
        # Calculate metrics
        user_metrics = get_activity_based_metrics()
        
        if user_metrics:
            print(f"✅ Activity calculation successful! Processed {len(user_metrics)} users")
            
            # Show sample metrics
            sample_user = list(user_metrics.values())[0]
            print(f"  Sample user: {sample_user['name']}")
            print(f"  Attendance rate: {sample_user['attendance_metrics']['attendance_rate']:.1%}")
            print(f"  Total commits: {sample_user['activity_metrics']['total_commits']}")
            print(f"  Total messages: {sample_user['activity_metrics']['total_messages']}")
            
            return True
        else:
            print("❌ No user metrics calculated")
            return False
            
    except Exception as e:
        print(f"❌ Activity calculation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scoring_engine():
    """Test the scoring engine with sample data"""
    print("\n🧪 Testing Scoring Engine...")
    
    try:
        from engine.scoring import DevLensKeywordScorer, process_metrics
        
        # Create sample developer data
        sample_developers = [
            {
                "name": "Alex Chen",
                "team": "Frontend",
                "commits": 45,
                "entropy": 12.5,
                "meetings": 15,
                "msgs": ["Fixed authentication bug", "Updated UI components", "Great work team!"],
                "comm_score": 8.5
            },
            {
                "name": "Sarah Johnson", 
                "team": "Backend",
                "commits": 62,
                "entropy": 18.3,
                "meetings": 12,
                "msgs": ["Refactored API endpoints", "Optimized database queries", "Deploy to staging"],
                "comm_score": 12.2
            }
        ]
        
        # Test scoring
        processed = process_metrics(sample_developers)
        
        if processed:
            print(f"✅ Scoring engine successful! Processed {len(processed)} developers")
            
            for dev in processed:
                print(f"  {dev['name']}: {dev['archetype']} (Impact: {dev['impact_score']}, Visibility: {dev['visibility_score']})")
            
            return True
        else:
            print("❌ No processed developers returned")
            return False
            
    except Exception as e:
        print(f"❌ Scoring engine failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 DEVLENS DATA PIPELINE TESTS")
    print("=" * 60)
    
    tests = [
        ("Data Generation", test_data_generation),
        ("Activity Calculation", test_activity_calculation), 
        ("Scoring Engine", test_scoring_engine)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your data pipeline is working correctly.")
        print("\nNext steps:")
        print("1. Run: python backend/scripts/run_complete_data_pipeline.py")
        print("2. Start backend: python backend/main.py")
        print("3. Start frontend: cd frontend && npm start")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()