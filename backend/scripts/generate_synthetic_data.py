#!/usr/bin/env python3
"""
Unified Synthetic Data Generator for DevLens
Generates consistent communication, execution, and HR data with proper relationships
"""

import json
import random
import math
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SyntheticDataGenerator:
    def __init__(self, seed=42):
        """Initialize with fixed seed for reproducible data"""
        random.seed(seed)
        np.random.seed(seed)
        
        # Configuration
        self.NUM_USERS = 25
        self.NUM_MESSAGES = 800
        self.NUM_COMMITS = 1200
        self.ANALYSIS_PERIOD_DAYS = 90
        
        # Date range
        self.start_time = datetime(2024, 5, 21, 8, 0, 0)
        self.end_time = self.start_time + timedelta(days=self.ANALYSIS_PERIOD_DAYS)
        
        # Team structure
        self.team_members = [
            {"id": f"teams_guid_{i:03}", "name": name, "team": team}
            for i, (name, team) in enumerate([
                ("Alex Chen", "Frontend"), ("Sarah Johnson", "Backend"), ("Mike Rodriguez", "DevOps"),
                ("Emily Davis", "Frontend"), ("James Wilson", "Backend"), ("Lisa Zhang", "QA"),
                ("David Kim", "Frontend"), ("Rachel Green", "Backend"), ("Tom Anderson", "DevOps"),
                ("Maria Garcia", "QA"), ("Kevin Lee", "Frontend"), ("Anna Smith", "Backend"),
                ("Chris Brown", "DevOps"), ("Jessica Taylor", "QA"), ("Ryan Murphy", "Frontend"),
                ("Sophie Wang", "Backend"), ("Daniel Clark", "DevOps"), ("Amy Liu", "QA"),
                ("Mark Thompson", "Frontend"), ("Grace Park", "Backend"), ("Jason Miller", "DevOps"),
                ("Olivia Chen", "QA"), ("Nathan Davis", "Frontend"), ("Emma Wilson", "Backend"),
                ("Lucas Garcia", "DevOps")
            ], 1)
        ]
        
        # Message templates by complexity
        self.message_templates = {
            "high_tech": [
                "Implemented OAuth2 JWT refresh token rotation mechanism",
                "Optimized database connection pooling - reduced latency by 40%",
                "Refactored microservices architecture for better scalability",
                "Fixed critical memory leak in Redis caching layer",
                "Deployed blue-green deployment pipeline with zero downtime",
                "Integrated GraphQL federation across multiple services",
                "Implemented distributed tracing with Jaeger and OpenTelemetry"
            ],
            "medium_tech": [
                "Updated API endpoints for user authentication",
                "Fixed bug in payment processing workflow",
                "Added unit tests for core business logic",
                "Reviewed PR for database migration scripts",
                "Updated Docker containers for staging environment",
                "Implemented error handling for external API calls"
            ],
            "low_tech": [
                "Updated documentation for new features",
                "Fixed minor UI styling issues",
                "Added logging statements for debugging",
                "Updated package dependencies",
                "Fixed typos in error messages"
            ],
            "social": [
                "Good morning team! ☀️",
                "Anyone available for a quick sync?",
                "Great work on the release! 🎉",
                "Thanks for the code review!",
                "Let's discuss this in our standup",
                "Coffee break anyone? ☕",
                "Have a great weekend team!"
            ]
        }
        
        # Repository and file structure
        self.repos = ["core-auth", "payment-gateway", "frontend-main", "docs-site", "api-gateway", "user-service"]
        
        self.file_types = {
            "Backend": [
                {"ext": ".py", "impact": 1.2, "path": "src/services/"},
                {"ext": ".js", "impact": 1.0, "path": "src/api/"},
                {"ext": ".sql", "impact": 0.9, "path": "migrations/"},
                {"ext": ".yaml", "impact": 0.7, "path": "config/"}
            ],
            "Frontend": [
                {"ext": ".tsx", "impact": 1.1, "path": "src/components/"},
                {"ext": ".css", "impact": 0.6, "path": "src/styles/"},
                {"ext": ".js", "impact": 1.0, "path": "src/utils/"},
                {"ext": ".json", "impact": 0.4, "path": "public/"}
            ],
            "DevOps": [
                {"ext": ".yml", "impact": 1.3, "path": ".github/workflows/"},
                {"ext": ".tf", "impact": 1.2, "path": "infrastructure/"},
                {"ext": ".sh", "impact": 1.0, "path": "scripts/"},
                {"ext": ".dockerfile", "impact": 1.1, "path": "docker/"}
            ],
            "QA": [
                {"ext": ".py", "impact": 0.8, "path": "tests/"},
                {"ext": ".js", "impact": 0.7, "path": "e2e/"},
                {"ext": ".md", "impact": 0.3, "path": "docs/"},
                {"ext": ".json", "impact": 0.5, "path": "test-data/"}
            ]
        }

    def generate_communication_data(self):
        """Generate realistic communication messages"""
        print("Generating communication data...")
        
        messages = []
        message_ids = []
        
        for i in range(1, self.NUM_MESSAGES + 1):
            msg_id = f"m_{i:04}"
            author = random.choice(self.team_members)
            
            # 25% chance this is a reply
            reply_to = random.choice(message_ids) if message_ids and random.random() < 0.25 else None
            
            # Select message type based on team
            if author["team"] in ["Backend", "DevOps"]:
                if random.random() < 0.5:
                    content = random.choice(self.message_templates["high_tech"])
                elif random.random() < 0.3:
                    content = random.choice(self.message_templates["medium_tech"])
                else:
                    content = random.choice(self.message_templates["social"])
            elif author["team"] == "Frontend":
                if random.random() < 0.4:
                    content = random.choice(self.message_templates["medium_tech"])
                elif random.random() < 0.3:
                    content = random.choice(self.message_templates["low_tech"])
                else:
                    content = random.choice(self.message_templates["social"])
            else:  # QA
                if random.random() < 0.3:
                    content = random.choice(self.message_templates["medium_tech"])
                elif random.random() < 0.4:
                    content = random.choice(self.message_templates["low_tech"])
                else:
                    content = random.choice(self.message_templates["social"])
            
            msg = {
                "id": msg_id,
                "replyToId": reply_to,
                "createdDateTime": (self.start_time + timedelta(hours=i * 0.3)).isoformat() + "Z",
                "from": {
                    "user": {
                        "id": author["id"],
                        "displayName": author["name"],
                        "team": author["team"]
                    }
                },
                "body": {
                    "contentType": "html",
                    "content": f"<div>{content}</div>"
                }
            }
            
            messages.append(msg)
            message_ids.append(msg_id)
        
        return messages

    def calculate_shannon_entropy(self, file_changes):
        """Calculate Shannon entropy based on distribution of effort across files"""
        if not file_changes:
            return 0.0
        
        total_changes = sum(changes for changes in file_changes.values())
        if total_changes == 0:
            return 0.0
        
        entropy = 0.0
        for file_path, changes in file_changes.items():
            if changes > 0:
                pi = changes / total_changes
                entropy -= pi * math.log2(pi)
        
        return entropy

    def generate_commit_files(self, author, repo):
        """Generate realistic file changes for a commit"""
        team_files = self.file_types[author["team"]]
        
        # Determine number of files to change (1-5 files per commit)
        num_files = random.choices([1, 2, 3, 4, 5], weights=[40, 30, 20, 8, 2])[0]
        
        file_changes = {}
        for _ in range(num_files):
            f_info = random.choice(team_files)
            
            # Generate unique file name
            file_id = random.randint(1, 100)
            file_name = f"{f_info['path']}{repo}_{file_id}{f_info['ext']}"
            
            # Generate realistic changes per file
            base_productivity = {"Backend": 1.2, "Frontend": 1.0, "DevOps": 1.4, "QA": 0.8}
            productivity_multiplier = base_productivity[author["team"]]
            individual_multiplier = random.uniform(0.7, 1.5)
            
            additions = int(random.randint(5, 80) * productivity_multiplier * individual_multiplier)
            deletions = int(random.randint(0, 40) * productivity_multiplier * individual_multiplier)
            total_changes = additions + deletions
            
            file_changes[file_name] = total_changes
        
        return file_changes

    def generate_execution_data(self):
        """Generate realistic Git commit data"""
        print("Generating execution data...")
        
        commits = []
        
        for i in range(1, self.NUM_COMMITS + 1):
            author = random.choice(self.team_members)
            repo = random.choice(self.repos)
            
            # Generate file changes for this commit
            file_changes = self.generate_commit_files(author, repo)
            
            # Calculate Shannon entropy based on file distribution
            entropy = self.calculate_shannon_entropy(file_changes)
            
            # Calculate total additions and deletions
            total_additions = 0
            total_deletions = 0
            
            files_data = []
            for file_path, total_changes in file_changes.items():
                # Distribute total changes between additions and deletions (roughly 70/30 split)
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
                "sha": f"sha_exec_{i:05}",
                "node_id": f"MDY6Q29tbWl0{i}",
                "commit": {
                    "author": {
                        "name": author["name"],
                        "email": f"{author['name'].lower().replace(' ', '.')}@company.com",
                        "date": (self.start_time + timedelta(hours=i * 0.5)).isoformat() + "Z"
                    },
                    "message": f"Update {len(file_changes)} files in {repo}",
                    "comment_count": random.randint(0, 3)
                },
                "url": f"https://api.github.com/repos/org/{repo}/commits/sha_{i}",
                "files": files_data,
                "devlens_meta": {
                    "teams_user_id": author["id"],
                    "team": author["team"],
                    "files_changed": len(file_changes),
                    "file_distribution": file_changes,
                    "stats": {
                        "additions": total_additions,
                        "deletions": total_deletions,
                        "total_entropy": entropy
                    }
                }
            }
            
            commits.append(commit)
        
        return commits

    def generate_hr_data(self):
        """Generate comprehensive HR and behavioral metrics"""
        print("Generating HR behavioral data...")
        
        hr_data = []
        total_work_days = self.ANALYSIS_PERIOD_DAYS - 26  # Exclude weekends
        
        for member in self.team_members:
            # Base personality traits that influence other metrics
            personality_traits = {
                "collaboration_tendency": random.uniform(0.3, 1.0),
                "knowledge_sharing_tendency": random.uniform(0.2, 1.0),
                "meeting_engagement": random.uniform(0.4, 1.0),
                "proactivity_level": random.uniform(0.3, 1.0),
                "reliability_factor": random.uniform(0.6, 1.0)
            }
            
            # Attendance & Leave Management
            leave_days = int(random.uniform(2, 15) * (1 - personality_traits["reliability_factor"]))
            sick_days = int(random.uniform(0, 8) * (1 - personality_traits["reliability_factor"]))
            attendance_rate = (total_work_days - leave_days - sick_days) / total_work_days
            
            # Meeting & Collaboration Metrics
            total_meetings = random.randint(40, 120)
            meetings_attended = int(total_meetings * attendance_rate * personality_traits["meeting_engagement"])
            meetings_organized = int(random.uniform(2, 15) * personality_traits["proactivity_level"])
            
            # Knowledge Sharing & Documentation
            wiki_contributions = int(random.uniform(5, 50) * personality_traits["knowledge_sharing_tendency"])
            documentation_updates = int(random.uniform(3, 25) * personality_traits["knowledge_sharing_tendency"])
            knowledge_base_articles = int(random.uniform(1, 12) * personality_traits["knowledge_sharing_tendency"])
            
            # Code Review & Collaboration
            code_reviews_given = int(random.uniform(10, 80) * personality_traits["collaboration_tendency"])
            code_reviews_received = int(random.uniform(8, 40))
            review_response_time_hours = random.uniform(2, 48) * (2 - personality_traits["collaboration_tendency"])
            
            # Additional metrics...
            hr_record = {
                "user_id": member["id"],
                "name": member["name"],
                "team": member["team"],
                "analysis_period": {
                    "start_date": self.start_time.date().isoformat(),
                    "end_date": self.end_time.date().isoformat(),
                    "total_days": self.ANALYSIS_PERIOD_DAYS
                },
                "attendance_metrics": {
                    "total_work_days": total_work_days,
                    "days_present": total_work_days - leave_days - sick_days,
                    "leave_days": leave_days,
                    "sick_days": sick_days,
                    "attendance_rate": round(attendance_rate, 3)
                },
                "collaboration_metrics": {
                    "meetings_attended": meetings_attended,
                    "meetings_organized": meetings_organized,
                    "meeting_attendance_rate": round(meetings_attended / total_meetings, 3),
                    "code_reviews_given": code_reviews_given,
                    "code_reviews_received": code_reviews_received,
                    "avg_review_response_time_hours": round(review_response_time_hours, 1)
                },
                "personality_indicators": {
                    "collaboration_score": round(personality_traits["collaboration_tendency"], 3),
                    "knowledge_sharing_score": round(personality_traits["knowledge_sharing_tendency"], 3),
                    "proactivity_score": round(personality_traits["proactivity_level"], 3),
                    "reliability_score": round(personality_traits["reliability_factor"], 3)
                }
            }
            
            hr_data.append(hr_record)
        
        return hr_data

    def generate_all_data(self):
        """Generate all synthetic data and save to files"""
        print("Starting synthetic data generation...")
        
        # Ensure data directory exists
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(data_dir, exist_ok=True)
        
        # Generate all datasets
        comm_data = self.generate_communication_data()
        exec_data = self.generate_execution_data()
        hr_data = self.generate_hr_data()
        
        # Save communication data
        comm_path = os.path.join(data_dir, "comm_mock_data.json")
        with open(comm_path, "w", encoding="utf-8") as f:
            json.dump(comm_data, f, indent=2)
        print(f"Communication data saved: {len(comm_data)} messages")
        
        # Save execution data
        exec_path = os.path.join(data_dir, "exec_mock_data.json")
        with open(exec_path, "w", encoding="utf-8") as f:
            json.dump(exec_data, f, indent=2)
        print(f"Execution data saved: {len(exec_data)} commits")
        
        # Save HR data
        hr_path = os.path.join(data_dir, "hr_behavioral_data.json")
        with open(hr_path, "w", encoding="utf-8") as f:
            json.dump(hr_data, f, indent=2)
        print(f"HR behavioral data saved: {len(hr_data)} team members")
        
        return {
            "communication": comm_path,
            "execution": exec_path,
            "hr_behavioral": hr_path
        }


if __name__ == "__main__":
    generator = SyntheticDataGenerator(seed=42)  # Fixed seed for reproducibility
    file_paths = generator.generate_all_data()
    
    print("\nSynthetic data generation complete!")
    print("Generated files:")
    for data_type, path in file_paths.items():
        print(f"  - {data_type}: {path}")