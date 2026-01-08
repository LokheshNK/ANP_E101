#!/usr/bin/env python3
"""
Complete DevLens Data Setup
Sets up companies, managers, teams, and developers with proper database integration
"""

import os
import sys
import subprocess
from pathlib import Path

def run_script(script_path, description, args=None):
    """Run a Python script and handle errors"""
    print(f"\n> {description}")
    print("-" * 60)
    
    try:
        cmd = [sys.executable, script_path]
        if args:
            cmd.extend(args)
            
        result = subprocess.run(cmd, capture_output=True, text=True, 
                              cwd=os.path.dirname(script_path))
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"SUCCESS: {description} completed")
            return True
        else:
            print(f"ERROR in {description}:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"FAILED to run {description}: {e}")
        return False

def main():
    """Main setup workflow"""
    print("DEVLENS COMPLETE DATA SETUP")
    print("=" * 50)
    print("This will create companies with managers, teams, and developers")
    print("Then export data for analytics compatibility")
    
    # Get script directory
    script_dir = Path(__file__).parent
    
    # Step 1: Generate company data (creates database entries)
    print("\nSTEP 1: Creating Companies and Teams")
    success1 = run_script(
        str(script_dir / "generate_company_data.py"),
        "Generate Company Database Structure"
    )
    
    if not success1:
        print("\nSetup failed at Step 1. Check errors above.")
        return
    
    # Step 2: Export to JSON files for analytics
    print("\nSTEP 2: Exporting Data for Analytics")
    success2 = run_script(
        str(script_dir / "export_database_to_json.py"),
        "Export Database to JSON Files"
    )
    
    if not success2:
        print("\nWarning: JSON export failed, but database is set up.")
        print("You can still use the application with database data.")
    
    # Step 3: Calculate activity metrics (optional)
    print("\nSTEP 3: Calculating Activity Metrics")
    success3 = run_script(
        str(script_dir / "calculate_attendance_from_activity.py"),
        "Calculate Activity-Based Metrics"
    )
    
    # Summary
    print("\n" + "=" * 50)
    print("SETUP SUMMARY")
    print("=" * 50)
    
    if success1:
        print("SUCCESS: Companies and teams created in database")
        
        # Show login information
        print("\nMANAGER LOGIN CREDENTIALS:")
        print("-" * 30)
        
        managers = [
            {"name": "Sarah Chen", "email": "sarah.chen@techcorp.com", "password": "manager123", "company": "TechCorp Solutions"},
            {"name": "Alex Rodriguez", "email": "alex@innovate.io", "password": "startup456", "company": "Innovate Dynamics"},
            {"name": "Jordan Kim", "email": "jordan.kim@agileworks.com", "password": "agile789", "company": "AgileWorks Inc"},
            {"name": "Morgan Taylor", "email": "morgan@cloudfirst.tech", "password": "cloud2024", "company": "CloudFirst Technologies"}
        ]
        
        for mgr in managers:
            print(f"Company: {mgr['company']}")
            print(f"  Email: {mgr['email']}")
            print(f"  Password: {mgr['password']}")
            print(f"  Manager: {mgr['name']}")
            print()
        
        print("NEXT STEPS:")
        print("1. Start backend server:")
        print("   python backend/main.py")
        print()
        print("2. Start frontend:")
        print("   cd frontend && npm start")
        print()
        print("3. Login with any manager credentials above")
        print("4. Explore your team's performance analytics!")
        
        if success2:
            print("\nBONUS: JSON files created for advanced analytics")
        
        if success3:
            print("BONUS: Activity metrics calculated")
    
    else:
        print("FAILED: Setup incomplete. Check error messages above.")


if __name__ == "__main__":
    main()