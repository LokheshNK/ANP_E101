#!/usr/bin/env python3
"""
Export Database to JSON Files
Exports database data to JSON files compatible with existing DevLens analytics
"""

import os
import sys
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DevLensDB

class DatabaseToJSONExporter:
    def __init__(self):
        self.db = DevLensDB()
        self.start_time = datetime(2024, 5, 21, 8, 0, 0)
        
    def export_communication_data(self, company_name):
        """Export communication data for a specific company"""
        developers = self.db.get_company_developers(company_name)
        
        messages = []
        message_id = 1
        
        for dev in developers:
            # Create user ID that matches the expected format
            user_id = f"teams_guid_{dev['name'].lower().replace(' ', '_')}"
            
            # Generate messages based on developer's message list
            dev_messages = dev.get('msgs', [])
            
            for i, msg_content in enumerate(dev_messages):
                # Calculate timestamp (spread over time period)
                hours_offset = (message_id * 0.3) + random.uniform(-2, 2)
                timestamp = self.start_time + timedelta(hours=hours_offset)
                
                message = {
                    "id": f"m_{message_id:04d}",
                    "replyToId": None,  # Could add reply logic later
                    "createdDateTime": timestamp.isoformat() + "Z",
                    "from": {
                        "user": {
                            "id": user_id,
                            "displayName": dev['name'],
                            "team": dev['team']
                        }
                    },
                    "body": {
                        "contentType": "html",
                        "content": f"<div>{msg_content}</div>"
                    }
                }
                
                messages.append(message)
                message_id += 1
        
        return messages
    
    def calculate_shannon_entropy(self, file_changes):
        """Calculate Shannon entropy for file distribution"""
        if not file_changes:
            return 0.0
        
        total_changes = sum(changes for changes in file_changes.values())
        if total_changes == 0:
            return 0.0
        
        import math
        entropy = 0.0
        for file_path, changes in file_changes.items():
            if changes > 0:
                pi = changes / total_changes
                entropy -= pi * math.log2(pi)
        
        return entropy
    
    def generate_commit_files(self, team, commits_count, total_entropy):
        """Generate realistic file changes that match the entropy"""
        
        # File types by team
        file_types = {
            "Backend": [".py", ".js", ".sql", ".yaml"],
            "Frontend": [".tsx", ".css", ".js", ".json"],
            "DevOps": [".yml", ".tf", ".sh", ".dockerfile"],
            "QA": [".py", ".js", ".md", ".json"],
            "Full Stack": [".py", ".tsx", ".js", ".json"],
            "Mobile": [".dart", ".swift", ".kt", ".js"],
            "Data Science": [".py", ".ipynb", ".sql", ".yaml"],
            "Platform": [".go", ".yaml", ".tf", ".sh"],
            "Infrastructure": [".tf", ".yaml", ".sh", ".json"],
            "Security": [".py", ".yaml", ".sh", ".json"],
            "API": [".py", ".js", ".yaml", ".json"]
        }
        
        extensions = file_types.get(team, [".py", ".js", ".json", ".md"])
        
        # Generate files to match target entropy
        target_entropy_per_commit = total_entropy / max(1, commits_count)
        
        file_changes = {}
        
        # Create diverse file distribution to achieve target entropy
        num_files = max(1, int(target_entropy_per_commit * 3))  # More files = higher entropy
        
        for i in range(num_files):
            ext = random.choice(extensions)
            file_path = f"src/{team.lower()}/module_{i}{ext}"
            
            # Vary file sizes to create entropy
            changes = random.randint(5, 100)
            file_changes[file_path] = changes
        
        return file_changes
    
    def export_execution_data(self, company_name):
        """Export Git execution data for a specific company"""
        developers = self.db.get_company_developers(company_name)
        
        commits = []
        commit_id = 1
        
        repos = ["core-service", "web-app", "mobile-app", "api-gateway", "data-pipeline"]
        
        for dev in developers:
            user_id = f"teams_guid_{dev['name'].lower().replace(' ', '_')}"
            dev_commits = dev.get('commits', 0)
            dev_entropy = dev.get('entropy', 0.0)
            
            # Generate individual commits for this developer
            for i in range(dev_commits):
                # Calculate timestamp
                hours_offset = (commit_id * 0.5) + random.uniform(-4, 4)
                timestamp = self.start_time + timedelta(hours=hours_offset)
                
                # Generate file changes for this commit
                entropy_per_commit = dev_entropy / max(1, dev_commits)
                file_changes = self.generate_commit_files(dev['team'], 1, entropy_per_commit)
                
                # Calculate actual entropy for this commit
                commit_entropy = self.calculate_shannon_entropy(file_changes)
                
                # Calculate additions and deletions
                total_additions = 0
                total_deletions = 0
                files_data = []
                
                for file_path, total_changes in file_changes.items():
                    file_additions = int(total_changes * random.uniform(0.6, 0.8))
                    file_deletions = total_changes - file_additions
                    
                    total_additions += file_additions
                    total_deletions += file_deletions
                    
                    files_data.append({
                        "filename": file_path,
                        "additions": file_additions,
                        "deletions": file_deletions,
                        "changes": total_changes
                    })
                
                commit = {
                    "sha": f"sha_exec_{commit_id:05d}",
                    "node_id": f"MDY6Q29tbWl0{commit_id}",
                    "commit": {
                        "author": {
                            "name": dev['name'],
                            "email": f"{dev['name'].lower().replace(' ', '.')}@{company_name.lower().replace(' ', '')}.com",
                            "date": timestamp.isoformat() + "Z"
                        },
                        "message": f"Update {len(file_changes)} files in {random.choice(repos)}",
                        "comment_count": random.randint(0, 3)
                    },
                    "url": f"https://api.github.com/repos/org/{random.choice(repos)}/commits/sha_{commit_id}",
                    "files": files_data,
                    "devlens_meta": {
                        "teams_user_id": user_id,
                        "team": dev['team'],
                        "files_changed": len(file_changes),
                        "file_distribution": file_changes,
                        "stats": {
                            "additions": total_additions,
                            "deletions": total_deletions,
                            "total_entropy": commit_entropy
                        }
                    }
                }
                
                commits.append(commit)
                commit_id += 1
        
        return commits
    
    def export_hr_data(self, company_name):
        """Export HR behavioral data for a specific company"""
        developers = self.db.get_company_developers(company_name)
        
        hr_data = []
        analysis_period_days = 90
        total_work_days = analysis_period_days - 26  # Exclude weekends
        
        for dev in developers:
            user_id = f"teams_guid_{dev['name'].lower().replace(' ', '_')}"
            
            # Base metrics from database
            commits = dev.get('commits', 0)
            meetings = dev.get('meetings', 0)
            messages = dev.get('msgs', [])
            
            # Calculate derived metrics
            # Attendance based on activity level
            activity_score = min(1.0, (commits + len(messages)) / 30.0)
            attendance_rate = 0.7 + (activity_score * 0.3)  # 70-100% range
            
            days_present = int(total_work_days * attendance_rate)
            leave_days = random.randint(2, 8)
            sick_days = random.randint(0, 4)
            
            # Collaboration metrics
            collaboration_score = min(1.0, len(messages) / 15.0)
            code_reviews_given = int(commits * random.uniform(0.3, 0.8))
            code_reviews_received = int(commits * random.uniform(0.2, 0.6))
            
            hr_record = {
                "user_id": user_id,
                "name": dev['name'],
                "team": dev['team'],
                "analysis_period": {
                    "start_date": self.start_time.date().isoformat(),
                    "end_date": (self.start_time + timedelta(days=analysis_period_days)).date().isoformat(),
                    "total_days": analysis_period_days
                },
                "attendance_metrics": {
                    "total_work_days": total_work_days,
                    "days_present": days_present,
                    "leave_days": leave_days,
                    "sick_days": sick_days,
                    "attendance_rate": round(attendance_rate, 3)
                },
                "collaboration_metrics": {
                    "meetings_attended": meetings,
                    "meetings_organized": random.randint(0, 5),
                    "meeting_attendance_rate": round(min(1.0, meetings / 15.0), 3),
                    "code_reviews_given": code_reviews_given,
                    "code_reviews_received": code_reviews_received,
                    "avg_review_response_time_hours": round(random.uniform(2, 48), 1)
                },
                "personality_indicators": {
                    "collaboration_score": round(collaboration_score, 3),
                    "knowledge_sharing_score": round(min(1.0, len(messages) / 20.0), 3),
                    "proactivity_score": round(min(1.0, commits / 25.0), 3),
                    "reliability_score": round(attendance_rate, 3)
                }
            }
            
            hr_data.append(hr_record)
        
        return hr_data
    
    def export_company_data(self, company_name, output_dir=None):
        """Export all data for a specific company"""
        
        if not output_dir:
            script_dir = Path(__file__).parent
            output_dir = script_dir.parent / "data"
        
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        print(f"Exporting data for: {company_name}")
        
        # Export communication data
        comm_data = self.export_communication_data(company_name)
        comm_path = output_dir / "comm_mock_data.json"
        with open(comm_path, "w", encoding="utf-8") as f:
            json.dump(comm_data, f, indent=2)
        print(f"  Communication data: {len(comm_data)} messages -> {comm_path}")
        
        # Export execution data
        exec_data = self.export_execution_data(company_name)
        exec_path = output_dir / "exec_mock_data.json"
        with open(exec_path, "w", encoding="utf-8") as f:
            json.dump(exec_data, f, indent=2)
        print(f"  Execution data: {len(exec_data)} commits -> {exec_path}")
        
        # Export HR data
        hr_data = self.export_hr_data(company_name)
        hr_path = output_dir / "hr_behavioral_data.json"
        with open(hr_path, "w", encoding="utf-8") as f:
            json.dump(hr_data, f, indent=2)
        print(f"  HR behavioral data: {len(hr_data)} team members -> {hr_path}")
        
        return {
            "communication": str(comm_path),
            "execution": str(exec_path),
            "hr_behavioral": str(hr_path)
        }
    
    def list_available_companies(self):
        """List all companies in the database"""
        companies = self.db.get_companies()
        
        print("Available companies:")
        for company_id, company_name in companies:
            developers = self.db.get_company_developers(company_name)
            print(f"  - {company_name} ({len(developers)} developers)")
        
        return [name for _, name in companies]


def main():
    """Main function"""
    print("DEVLENS DATABASE TO JSON EXPORTER")
    print("=" * 50)
    
    exporter = DatabaseToJSONExporter()
    
    # List available companies
    companies = exporter.list_available_companies()
    
    if not companies:
        print("\nNo companies found in database!")
        print("Run: python backend/scripts/generate_company_data.py")
        return
    
    # Export data for first company (or specify company name)
    import sys
    if len(sys.argv) > 1:
        company_name = sys.argv[1]
        if company_name not in companies:
            print(f"\nCompany '{company_name}' not found!")
            print(f"Available: {', '.join(companies)}")
            return
    else:
        company_name = companies[0]  # Use first company
    
    print(f"\nExporting data for: {company_name}")
    print("-" * 30)
    
    # Export the data
    file_paths = exporter.export_company_data(company_name)
    
    print(f"\nExport complete! Files created:")
    for data_type, path in file_paths.items():
        print(f"  {data_type}: {path}")
    
    print(f"\nNext steps:")
    print(f"1. Start backend: python backend/main.py")
    print(f"2. Login as manager for {company_name}")
    print(f"3. View analytics dashboard")


if __name__ == "__main__":
    main()