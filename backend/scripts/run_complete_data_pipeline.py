#!/usr/bin/env python3
"""
Complete Data Pipeline for DevLens
Generates synthetic data and calculates all metrics in one go
"""

import os
import sys
import subprocess
from pathlib import Path

def run_script(script_path, description):
    """Run a Python script and handle errors"""
    print(f"\n> {description}")
    print("-" * 60)
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, cwd=os.path.dirname(script_path))
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"SUCCESS: {description} completed successfully")
            return True
        else:
            print(f"ERROR in {description}:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"FAILED to run {description}: {e}")
        return False

def main():
    """Run the complete data pipeline"""
    print("DEVLENS COMPLETE DATA PIPELINE")
    print("=" * 80)
    
    # Get script directory
    script_dir = Path(__file__).parent
    
    # Define pipeline steps
    pipeline_steps = [
        {
            "script": script_dir / "generate_synthetic_data.py",
            "description": "Generating Synthetic Data (Communication, Execution, HR)"
        },
        {
            "script": script_dir / "calculate_attendance_from_activity.py", 
            "description": "Calculating Activity-Based Metrics"
        },
        {
            "script": script_dir / "load_synthetic_data_to_db.py",
            "description": "Loading Synthetic Data into Database"
        }
    ]
    
    # Run pipeline
    success_count = 0
    for step in pipeline_steps:
        if run_script(str(step["script"]), step["description"]):
            success_count += 1
        else:
            print(f"\nWARNING: Pipeline stopped due to error in: {step['description']}")
            break
    
    # Summary
    print("\n" + "=" * 80)
    print("PIPELINE SUMMARY")
    print("=" * 80)
    
    if success_count == len(pipeline_steps):
        print("SUCCESS: All pipeline steps completed successfully!")
        
        # Show generated files
        data_dir = script_dir.parent / "data"
        if data_dir.exists():
            print(f"\nGenerated files in {data_dir}:")
            for file in data_dir.glob("*.json"):
                size_kb = file.stat().st_size / 1024
                print(f"  - {file.name} ({size_kb:.1f} KB)")
        
        print("\nNext steps:")
        print("  1. Start the backend server: python backend/main.py")
        print("  2. Start the frontend: cd frontend && npm start")
        print("  3. Login with: manager@devlens.com / demo123")
        print("  4. Company: DevLens Synthetic Corp")
        
    else:
        print(f"WARNING: Pipeline partially completed: {success_count}/{len(pipeline_steps)} steps")
        print("Check the error messages above for troubleshooting.")

if __name__ == "__main__":
    main()