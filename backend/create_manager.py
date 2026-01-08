#!/usr/bin/env python3
"""
Script to create a new manager in the DevLens database
"""

from database import DevLensDB

def create_new_manager():
    db = DevLensDB()
    
    print("=== DevLens Manager Creation ===")
    print()
    
    # Get manager details
    email = input("Enter manager email: ").strip()
    password = input("Enter password: ").strip()
    name = input("Enter manager name: ").strip()
    role = input("Enter role (e.g., Engineering Manager, CTO): ").strip()
    company = input("Enter company name: ").strip()
    
    print(f"\nCreating manager account for {name} at {company}...")
    
    # Create manager
    success = db.create_manager(email, password, name, role, company)
    
    if success:
        print(f"\n✅ Manager '{name}' created successfully!")
        print(f"   Email: {email}")
        print(f"   Company: {company}")
        print(f"   Role: {role}")
        print("\n🎉 Sample employees have been automatically generated for your company!")
        print("   • 12-18 diverse employees across 3-4 teams")
        print("   • Varied performance profiles (high performers, communicators, specialists, etc.)")
        print("   • Realistic commit patterns and meeting schedules")
        print("\nYou can now login with these credentials and see your team's analytics.")
    else:
        print(f"\n❌ Failed to create manager. Email '{email}' might already exist.")

def add_developer():
    db = DevLensDB()
    
    print("=== Add Developer ===")
    print()
    
    name = input("Enter developer name: ").strip()
    team = input("Enter team name: ").strip()
    company = input("Enter company name: ").strip()
    commits = int(input("Enter number of commits (default 0): ") or "0")
    entropy = float(input("Enter entropy/complexity (0.0-1.0, default 0.5): ") or "0.5")
    meetings = int(input("Enter meetings per week (default 0): ") or "0")
    
    messages = []
    print("Enter messages (press Enter twice to finish):")
    while True:
        msg = input("Message: ").strip()
        if not msg:
            break
        messages.append(msg)
    
    success = db.add_developer(name, team, company, commits, entropy, meetings, messages)
    
    if success:
        print(f"\n✅ Developer '{name}' added successfully to {team} team at {company}!")
    else:
        print(f"\n❌ Failed to add developer.")

def main():
    while True:
        print("\n=== DevLens Database Management ===")
        print("1. Create new manager (with auto-generated employees)")
        print("2. Add individual developer")
        print("3. View company profiles demo")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            create_new_manager()
        elif choice == "2":
            add_developer()
        elif choice == "3":
            from demo_companies import show_company_profiles, show_company_culture_analysis
            show_company_profiles()
            show_company_culture_analysis()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()