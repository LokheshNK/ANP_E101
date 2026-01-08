#!/usr/bin/env python3
"""
Load synthetic data into DevLens database
Replaces hardcoded sample data with generated synthetic data
"""

import os
import sys
import json
import sqlite3
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DevLensDB

class SyntheticDataLoader:
    def __init__(self):
        self.db = DevLensDB()
        
        # Get paths to synthetic data files
        script_dir = Path(__file__).parent
        self.data_dir = script_dir.parent / "data"
        
        self.comm_data_path = self.data_dir / "comm_mock_data.json"
        self.exec_data_path = self.data_dir / "exec_mock_data.json"
        self.hr_data_path = self.data_dir / "hr_behavioral_data.json"
        self.activity_data_path = self.data_dir / "activity_based_metrics.json"

    def load_synthetic_data_files(self):
        """Load all synthetic data files"""
        print("Loading synthetic data files...")
        
        # Load communication data
        with open(self.comm_data_path, 'r', encoding='utf-8') as f:
            comm_data = json.load(f)
        print(f"Loaded {len(comm_data)} communication messages")
        
        # Load execution data
        with open(self.exec_data_path, 'r', encoding='utf-8') as f:
            exec_data = json.load(f)
        print(f"Loaded {len(exec_data)} git commits")
        
        # Load HR behavioral data
        with open(self.hr_data_path, 'r', encoding='utf-8') as f:
            hr_data = json.load(f)
        print(f"Loaded {len(hr_data)} HR records")
        
        # Load activity-based metrics
        with open(self.activity_data_path, 'r', encoding='utf-8') as f:
            activity_data = json.load(f)
        print(f"Loaded {len(activity_data)} activity metrics")
        
        return comm_data, exec_data, hr_data, activity_data

    def clear_existing_data(self):
        """Clear existing sample data from database"""
        print("Clearing existing sample data...")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Clear in reverse order due to foreign key constraints
        cursor.execute("DELETE FROM settings")
        cursor.execute("DELETE FROM developers")
        cursor.execute("DELETE FROM teams")
        cursor.execute("DELETE FROM managers")
        cursor.execute("DELETE FROM companies")
        
        # Reset auto-increment counters
        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('companies', 'managers', 'teams', 'developers', 'settings')")
        
        conn.commit()
        conn.close()
        
        print("Existing data cleared")

    def create_synthetic_company_structure(self, hr_data):
        """Create company structure based on synthetic data"""
        print("Creating synthetic company structure...")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Create the synthetic company
        company_name = "DevLens Synthetic Corp"
        cursor.execute("INSERT INTO companies (name) VALUES (?)", (company_name,))
        company_id = cursor.lastrowid
        
        # Create a manager for the synthetic company
        manager_email = "manager@devlens.com"
        manager_password = self.db.hash_password("demo123")
        manager_name = "Demo Manager"
        
        cursor.execute('''
            INSERT INTO managers (email, password_hash, name, role, company_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (manager_email, manager_password, manager_name, "Engineering Manager", company_id))
        manager_id = cursor.lastrowid
        
        # Extract unique teams from HR data
        teams = set()
        for person in hr_data:
            teams.add(person['team'])
        
        # Create teams
        team_ids = {}
        for team_name in teams:
            cursor.execute("INSERT INTO teams (name, company_id) VALUES (?, ?)", (team_name, company_id))
            team_ids[team_name] = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        print(f"Created company '{company_name}' with {len(teams)} teams")
        return company_id, manager_id, team_ids

    def aggregate_user_data(self, comm_data, exec_data, hr_data, activity_data):
        """Aggregate data by user from all sources"""
        print("Aggregating user data from all sources...")
        
        # Create user lookup by ID
        users = {}
        
        # Start with HR data as the base (has all users)
        for hr_record in hr_data:
            user_id = hr_record['user_id']
            users[user_id] = {
                'name': hr_record['name'],
                'team': hr_record['team'],
                'commits': 0,
                'entropy': 0.0,
                'meetings': hr_record['collaboration_metrics']['meetings_attended'],
                'messages': []
            }
        
        # Add commit data
        commit_stats = {}
        for commit in exec_data:
            user_id = commit['devlens_meta']['teams_user_id']
            if user_id not in commit_stats:
                commit_stats[user_id] = {
                    'total_commits': 0,
                    'total_entropy': 0.0
                }
            
            commit_stats[user_id]['total_commits'] += 1
            commit_stats[user_id]['total_entropy'] += commit['devlens_meta']['stats']['total_entropy']
        
        # Apply commit stats to users
        for user_id, stats in commit_stats.items():
            if user_id in users:
                users[user_id]['commits'] = stats['total_commits']
                users[user_id]['entropy'] = stats['total_entropy']
        
        # Add communication data
        user_messages = {}
        for message in comm_data:
            user_id = message['from']['user']['id']
            if user_id not in user_messages:
                user_messages[user_id] = []
            
            # Extract clean message content
            content = message['body']['content']
            # Remove HTML tags
            import re
            clean_content = re.sub(r'<[^>]+>', '', content)
            user_messages[user_id].append(clean_content)
        
        # Apply messages to users
        for user_id, messages in user_messages.items():
            if user_id in users:
                users[user_id]['messages'] = messages
        
        print(f"Aggregated data for {len(users)} users")
        return users

    def insert_synthetic_developers(self, company_id, team_ids, users):
        """Insert synthetic developers into database"""
        print("Inserting synthetic developers...")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        inserted_count = 0
        for user_id, user_data in users.items():
            team_id = team_ids.get(user_data['team'])
            if not team_id:
                print(f"Warning: Team '{user_data['team']}' not found for user {user_data['name']}")
                continue
            
            messages_json = json.dumps(user_data['messages'])
            
            cursor.execute('''
                INSERT INTO developers (name, team_id, company_id, commits, entropy, meetings, messages)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_data['name'],
                team_id,
                company_id,
                user_data['commits'],
                user_data['entropy'],
                user_data['meetings'],
                messages_json
            ))
            
            inserted_count += 1
        
        conn.commit()
        conn.close()
        
        print(f"Inserted {inserted_count} synthetic developers")
        return inserted_count

    def create_manager_settings(self, manager_id):
        """Create default settings for the synthetic manager"""
        print("Creating manager settings...")
        
        success = self.db.create_default_settings_for_manager(
            manager_id=manager_id,
            manager_email="manager@devlens.com"
        )
        
        if success:
            print("Manager settings created successfully")
        else:
            print("Warning: Failed to create manager settings")

    def load_all_synthetic_data(self):
        """Complete process to load synthetic data into database"""
        print("=" * 60)
        print("LOADING SYNTHETIC DATA INTO DATABASE")
        print("=" * 60)
        
        try:
            # Check if synthetic data files exist
            if not all([
                self.comm_data_path.exists(),
                self.exec_data_path.exists(),
                self.hr_data_path.exists(),
                self.activity_data_path.exists()
            ]):
                print("ERROR: Synthetic data files not found!")
                print("Please run: python backend/scripts/run_complete_data_pipeline.py")
                return False
            
            # Load synthetic data files
            comm_data, exec_data, hr_data, activity_data = self.load_synthetic_data_files()
            
            # Clear existing data
            self.clear_existing_data()
            
            # Create company structure
            company_id, manager_id, team_ids = self.create_synthetic_company_structure(hr_data)
            
            # Aggregate user data from all sources
            users = self.aggregate_user_data(comm_data, exec_data, hr_data, activity_data)
            
            # Insert developers
            developer_count = self.insert_synthetic_developers(company_id, team_ids, users)
            
            # Create manager settings
            self.create_manager_settings(manager_id)
            
            print("\n" + "=" * 60)
            print("SYNTHETIC DATA LOADING COMPLETE!")
            print("=" * 60)
            print(f"Company: DevLens Synthetic Corp")
            print(f"Teams: {len(team_ids)}")
            print(f"Developers: {developer_count}")
            print(f"Manager: manager@devlens.com (password: demo123)")
            print("\nYou can now:")
            print("1. Start the backend: python backend/main.py")
            print("2. Start the frontend: cd frontend && npm start")
            print("3. Login with: manager@devlens.com / demo123")
            print("4. Company: DevLens Synthetic Corp")
            
            return True
            
        except Exception as e:
            print(f"ERROR loading synthetic data: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main function"""
    loader = SyntheticDataLoader()
    success = loader.load_all_synthetic_data()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()