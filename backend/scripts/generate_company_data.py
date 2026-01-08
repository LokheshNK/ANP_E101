#!/usr/bin/env python3
"""
Company-Based Data Generator for DevLens
Generates data that integrates with the existing database structure
Creates companies, managers, teams, and developers with proper relationships
"""

import os
import sys
import json
import random
import math
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DevLensDB

class CompanyDataGenerator:
    def __init__(self, seed=42):
        """Initialize with fixed seed for reproducible data"""
        random.seed(seed)
        
        # Initialize database
        self.db = DevLensDB()
        
        # Configuration
        self.start_time = datetime(2024, 5, 21, 8, 0, 0)
        self.end_time = self.start_time + timedelta(days=90)
        
        # Company templates with different organizational cultures
        self.company_templates = [
            {
                "name": "TechCorp Solutions",
                "culture": "enterprise",
                "manager": {
                    "name": "Sarah Chen",
                    "email": "sarah.chen@techcorp.com",
                    "password": "manager123",
                    "role": "Engineering Director"
                },
                "teams": ["Backend", "Frontend", "DevOps", "QA"],
                "size": "large"  # 15-20 developers
            },
            {
                "name": "Innovate Dynamics", 
                "culture": "startup",
                "manager": {
                    "name": "Alex Rodriguez",
                    "email": "alex@innovate.io",
                    "password": "startup456",
                    "role": "CTO"
                },
                "teams": ["Full Stack", "Mobile", "Data Science"],
                "size": "medium"  # 10-15 developers
            },
            {
                "name": "AgileWorks Inc",
                "culture": "agile",
                "manager": {
                    "name": "Jordan Kim",
                    "email": "jordan.kim@agileworks.com", 
                    "password": "agile789",
                    "role": "Development Manager"
                },
                "teams": ["Frontend", "Backend", "Platform", "Security"],
                "size": "large"  # 15-20 developers
            },
            {
                "name": "CloudFirst Technologies",
                "culture": "cloud_native",
                "manager": {
                    "name": "Morgan Taylor",
                    "email": "morgan@cloudfirst.tech",
                    "password": "cloud2024",
                    "role": "VP Engineering"
                },
                "teams": ["Platform", "Infrastructure", "Security", "API"],
                "size": "medium"  # 10-15 developers
            }
        ]
        
        # Developer name pool
        self.developer_names = [
            "Alex Chen", "Jordan Smith", "Taylor Johnson", "Casey Williams", "Morgan Brown",
            "Riley Davis", "Avery Miller", "Quinn Wilson", "Sage Moore", "River Taylor",
            "Phoenix Anderson", "Skylar Thomas", "Rowan Jackson", "Ember White", "Sage Harris",
            "Nova Martin", "Kai Thompson", "Zara Garcia", "Finn Martinez", "Luna Robinson",
            "Orion Clark", "Maya Rodriguez", "Leo Lewis", "Aria Lee", "Zoe Walker",
            "Eli Hall", "Nora Allen", "Max Young", "Ivy Hernandez", "Sam King"
        ]
        
        # Message templates by culture and role
        self.message_templates = {
            "enterprise": {
                "high_tech": [
                    "Completed enterprise security audit for authentication service",
                    "Implemented SOC2 compliance measures in data processing pipeline", 
                    "Optimized database connection pooling for high-availability setup",
                    "Deployed blue-green deployment strategy with zero downtime",
                    "Refactored legacy monolith into microservices architecture"
                ],
                "medium_tech": [
                    "Updated API documentation for client integration",
                    "Fixed critical bug in payment processing workflow",
                    "Added comprehensive unit tests for core business logic",
                    "Reviewed and approved database migration scripts",
                    "Updated Docker containers for staging environment"
                ],
                "social": [
                    "Good morning team! Ready for today's sprint review",
                    "Great work on the quarterly release everyone!",
                    "Thanks for the thorough code review",
                    "Let's discuss this in our architecture meeting",
                    "Excellent collaboration on the enterprise client project"
                ]
            },
            "startup": {
                "high_tech": [
                    "Shipped MVP feature in record time - 2 days!",
                    "Implemented real-time analytics with 99.9% uptime",
                    "Built scalable ML pipeline processing 1M+ events/day",
                    "Optimized API response time by 80% with caching layer",
                    "Created automated deployment pipeline from scratch"
                ],
                "medium_tech": [
                    "Fixed critical user-reported bug in mobile app",
                    "Added A/B testing framework for feature experiments",
                    "Implemented user authentication with social login",
                    "Updated payment integration for international markets",
                    "Built admin dashboard for customer support team"
                ],
                "social": [
                    "Crushing it today team! 🚀",
                    "Who's up for a quick brainstorming session?",
                    "Amazing progress on the product roadmap!",
                    "Coffee chat anyone? ☕",
                    "Love the energy in today's standup!"
                ]
            },
            "agile": {
                "high_tech": [
                    "Completed sprint goal: microservices communication layer",
                    "Implemented continuous integration with automated testing",
                    "Refactored codebase following SOLID principles",
                    "Built event-driven architecture for better scalability",
                    "Optimized database queries reducing load time by 60%"
                ],
                "medium_tech": [
                    "Updated user stories based on stakeholder feedback",
                    "Fixed bugs identified in sprint retrospective",
                    "Added feature flags for gradual rollout strategy",
                    "Implemented error tracking and monitoring system",
                    "Created API endpoints for new mobile features"
                ],
                "social": [
                    "Great retrospective insights today!",
                    "Ready for sprint planning tomorrow",
                    "Thanks for the pair programming session",
                    "Loving our team velocity this sprint",
                    "Excellent demo in the sprint review!"
                ]
            },
            "cloud_native": {
                "high_tech": [
                    "Deployed Kubernetes cluster with auto-scaling enabled",
                    "Implemented service mesh for microservices communication",
                    "Built CI/CD pipeline with GitOps workflow",
                    "Optimized cloud costs by 40% through resource optimization",
                    "Implemented distributed tracing across all services"
                ],
                "medium_tech": [
                    "Updated Terraform modules for infrastructure as code",
                    "Fixed container security vulnerabilities",
                    "Added monitoring and alerting for critical services",
                    "Implemented backup and disaster recovery procedures",
                    "Updated cloud security policies and access controls"
                ],
                "social": [
                    "Great work on the cloud migration!",
                    "Infrastructure is running smoothly",
                    "Thanks for the on-call support last night",
                    "Excellent troubleshooting on the outage",
                    "Love how our monitoring caught that issue early"
                ]
            }
        }

    def generate_developer_profile(self, culture, team, archetype=None):
        """Generate a realistic developer profile based on company culture and team"""
        
        # Define archetypes with culture-specific variations
        if not archetype:
            if culture == "enterprise":
                archetype = random.choices([
                    "senior_specialist",    # High impact, low visibility (Hidden Gems)
                    "team_lead",           # High impact, high visibility  
                    "steady_contributor",  # Medium impact, medium visibility
                    "process_focused",     # Low impact, high visibility
                    "junior_dev"          # Low impact, low visibility
                ], weights=[15, 20, 40, 15, 10])[0]
            elif culture == "startup":
                archetype = random.choices([
                    "full_stack_hero",     # Very high impact, medium visibility
                    "growth_hacker",       # High impact, high visibility
                    "rapid_prototyper",    # Medium impact, low visibility
                    "customer_focused",    # Medium impact, high visibility
                    "learning_fast"       # Low impact, medium visibility
                ], weights=[25, 20, 25, 20, 10])[0]
            elif culture == "agile":
                archetype = random.choices([
                    "scrum_master_dev",    # Medium impact, very high visibility
                    "technical_lead",      # High impact, high visibility
                    "story_implementer",   # Medium impact, medium visibility
                    "quality_advocate",    # Medium impact, high visibility
                    "continuous_learner"  # Low impact, medium visibility
                ], weights=[15, 25, 35, 15, 10])[0]
            else:  # cloud_native
                archetype = random.choices([
                    "platform_engineer",   # Very high impact, low visibility (Hidden Gems)
                    "devops_specialist",   # High impact, medium visibility
                    "reliability_engineer", # High impact, low visibility (Hidden Gems)
                    "automation_expert",   # Medium impact, medium visibility
                    "cloud_architect"     # High impact, high visibility
                ], weights=[20, 25, 20, 20, 15])[0]
        
        # Generate profile based on archetype
        profile = self._get_archetype_profile(archetype, culture, team)
        
        return profile

    def _get_archetype_profile(self, archetype, culture, team):
        """Get specific profile characteristics for each archetype"""
        
        profiles = {
            # Enterprise archetypes
            "senior_specialist": {
                "commits": (18, 25), "entropy": (0.85, 0.95), "meetings": (1, 4),
                "message_types": {"high_tech": 0.7, "medium_tech": 0.2, "social": 0.1},
                "message_count": (2, 5)
            },
            "team_lead": {
                "commits": (12, 18), "entropy": (0.7, 0.85), "meetings": (8, 15),
                "message_types": {"high_tech": 0.4, "medium_tech": 0.3, "social": 0.3},
                "message_count": (8, 15)
            },
            "steady_contributor": {
                "commits": (10, 16), "entropy": (0.6, 0.8), "meetings": (5, 10),
                "message_types": {"high_tech": 0.3, "medium_tech": 0.5, "social": 0.2},
                "message_count": (4, 8)
            },
            "process_focused": {
                "commits": (5, 10), "entropy": (0.3, 0.5), "meetings": (12, 20),
                "message_types": {"high_tech": 0.1, "medium_tech": 0.3, "social": 0.6},
                "message_count": (10, 18)
            },
            "junior_dev": {
                "commits": (3, 8), "entropy": (0.2, 0.4), "meetings": (6, 12),
                "message_types": {"high_tech": 0.1, "medium_tech": 0.4, "social": 0.5},
                "message_count": (5, 10)
            },
            
            # Startup archetypes
            "full_stack_hero": {
                "commits": (25, 35), "entropy": (0.9, 0.98), "meetings": (2, 5),
                "message_types": {"high_tech": 0.8, "medium_tech": 0.15, "social": 0.05},
                "message_count": (3, 6)
            },
            "growth_hacker": {
                "commits": (15, 22), "entropy": (0.7, 0.85), "meetings": (6, 12),
                "message_types": {"high_tech": 0.5, "medium_tech": 0.3, "social": 0.2},
                "message_count": (8, 15)
            },
            "rapid_prototyper": {
                "commits": (20, 28), "entropy": (0.6, 0.8), "meetings": (2, 6),
                "message_types": {"high_tech": 0.6, "medium_tech": 0.3, "social": 0.1},
                "message_count": (2, 5)
            },
            "customer_focused": {
                "commits": (8, 15), "entropy": (0.5, 0.7), "meetings": (10, 18),
                "message_types": {"high_tech": 0.2, "medium_tech": 0.4, "social": 0.4},
                "message_count": (12, 20)
            },
            "learning_fast": {
                "commits": (6, 12), "entropy": (0.4, 0.6), "meetings": (8, 14),
                "message_types": {"high_tech": 0.2, "medium_tech": 0.5, "social": 0.3},
                "message_count": (6, 12)
            },
            
            # Agile archetypes
            "scrum_master_dev": {
                "commits": (8, 14), "entropy": (0.5, 0.7), "meetings": (15, 25),
                "message_types": {"high_tech": 0.2, "medium_tech": 0.3, "social": 0.5},
                "message_count": (15, 25)
            },
            "technical_lead": {
                "commits": (15, 22), "entropy": (0.8, 0.9), "meetings": (10, 16),
                "message_types": {"high_tech": 0.6, "medium_tech": 0.25, "social": 0.15},
                "message_count": (10, 18)
            },
            "story_implementer": {
                "commits": (12, 18), "entropy": (0.6, 0.8), "meetings": (6, 12),
                "message_types": {"high_tech": 0.4, "medium_tech": 0.4, "social": 0.2},
                "message_count": (6, 12)
            },
            "quality_advocate": {
                "commits": (8, 14), "entropy": (0.5, 0.7), "meetings": (12, 18),
                "message_types": {"high_tech": 0.3, "medium_tech": 0.5, "social": 0.2},
                "message_count": (10, 16)
            },
            "continuous_learner": {
                "commits": (6, 12), "entropy": (0.4, 0.6), "meetings": (8, 14),
                "message_types": {"high_tech": 0.3, "medium_tech": 0.4, "social": 0.3},
                "message_count": (6, 12)
            },
            
            # Cloud Native archetypes
            "platform_engineer": {
                "commits": (20, 28), "entropy": (0.9, 0.98), "meetings": (1, 4),
                "message_types": {"high_tech": 0.8, "medium_tech": 0.15, "social": 0.05},
                "message_count": (2, 4)
            },
            "devops_specialist": {
                "commits": (16, 24), "entropy": (0.8, 0.9), "meetings": (4, 8),
                "message_types": {"high_tech": 0.7, "medium_tech": 0.2, "social": 0.1},
                "message_count": (4, 8)
            },
            "reliability_engineer": {
                "commits": (18, 25), "entropy": (0.85, 0.95), "meetings": (2, 6),
                "message_types": {"high_tech": 0.75, "medium_tech": 0.2, "social": 0.05},
                "message_count": (3, 6)
            },
            "automation_expert": {
                "commits": (14, 20), "entropy": (0.7, 0.85), "meetings": (6, 10),
                "message_types": {"high_tech": 0.6, "medium_tech": 0.3, "social": 0.1},
                "message_count": (5, 10)
            },
            "cloud_architect": {
                "commits": (12, 18), "entropy": (0.8, 0.9), "meetings": (8, 14),
                "message_types": {"high_tech": 0.6, "medium_tech": 0.25, "social": 0.15},
                "message_count": (8, 15)
            }
        }
        
        base_profile = profiles.get(archetype, profiles["steady_contributor"])
        
        # Generate actual values
        commits = random.randint(*base_profile["commits"])
        entropy = random.uniform(*base_profile["entropy"])
        meetings = random.randint(*base_profile["meetings"])
        
        # Generate messages based on type distribution
        message_count = random.randint(*base_profile["message_count"])
        messages = []
        
        templates = self.message_templates[culture]
        type_dist = base_profile["message_types"]
        
        for _ in range(message_count):
            msg_type = random.choices(
                ["high_tech", "medium_tech", "social"],
                weights=[type_dist["high_tech"], type_dist["medium_tech"], type_dist["social"]]
            )[0]
            
            message = random.choice(templates[msg_type])
            messages.append(message)
        
        return {
            "commits": commits,
            "entropy": entropy,
            "meetings": meetings,
            "messages": messages,
            "archetype": archetype
        }

    def create_company_with_data(self, company_template):
        """Create a complete company with manager, teams, and developers"""
        
        print(f"Creating company: {company_template['name']}")
        
        # Create company and manager
        try:
            manager_id = self.db.create_company_and_manager(
                company_name=company_template["name"],
                manager_email=company_template["manager"]["email"],
                manager_password=self.db.hash_password(company_template["manager"]["password"]),
                manager_name=company_template["manager"]["name"]
            )
            
            print(f"  Manager created: {company_template['manager']['name']} (ID: {manager_id})")
            
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                print(f"  Company/Manager already exists, skipping...")
                return False
            else:
                print(f"  Error creating company: {e}")
                return False
        
        # Determine company size
        if company_template["size"] == "large":
            num_developers = random.randint(15, 20)
        elif company_template["size"] == "medium":
            num_developers = random.randint(10, 15)
        else:
            num_developers = random.randint(6, 10)
        
        # Create developers
        used_names = set()
        developers_created = 0
        
        for i in range(num_developers):
            # Get unique name
            while True:
                name = random.choice(self.developer_names)
                if name not in used_names:
                    used_names.add(name)
                    break
            
            # Assign to team
            team = random.choice(company_template["teams"])
            
            # Generate profile
            profile = self.generate_developer_profile(
                culture=company_template["culture"],
                team=team
            )
            
            # Add developer to database
            success = self.db.add_developer(
                name=name,
                team_name=team,
                company_name=company_template["name"],
                commits=profile["commits"],
                entropy=profile["entropy"],
                meetings=profile["meetings"],
                messages=profile["messages"]
            )
            
            if success:
                developers_created += 1
                print(f"    Added {name} to {team} team ({profile['archetype']})")
        
        print(f"  Created {developers_created} developers across {len(company_template['teams'])} teams")
        return True

    def generate_all_companies(self):
        """Generate all company data"""
        print("Generating company-based data for DevLens...")
        print("=" * 60)
        
        companies_created = 0
        
        for template in self.company_templates:
            if self.create_company_with_data(template):
                companies_created += 1
            print()
        
        print("=" * 60)
        print(f"Company generation complete!")
        print(f"Created {companies_created} companies with managers and teams")
        
        # Show summary
        self.show_data_summary()
        
        return companies_created > 0

    def show_data_summary(self):
        """Show a summary of generated data"""
        print("\nDATA SUMMARY:")
        print("-" * 40)
        
        companies = self.db.get_companies()
        
        for company_id, company_name in companies:
            developers = self.db.get_company_developers(company_name)
            
            if developers:  # Only show companies with developers
                print(f"\n{company_name}:")
                print(f"  Total Developers: {len(developers)}")
                
                # Group by team
                teams = {}
                for dev in developers:
                    team = dev['team']
                    if team not in teams:
                        teams[team] = []
                    teams[team].append(dev)
                
                for team_name, team_devs in teams.items():
                    avg_commits = sum(d['commits'] for d in team_devs) / len(team_devs)
                    avg_entropy = sum(d['entropy'] for d in team_devs) / len(team_devs)
                    print(f"    {team_name}: {len(team_devs)} devs (avg: {avg_commits:.1f} commits, {avg_entropy:.2f} entropy)")

    def reset_database(self):
        """Reset database to clean state (for testing)"""
        print("Resetting database...")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Delete all data
        cursor.execute("DELETE FROM developers")
        cursor.execute("DELETE FROM teams") 
        cursor.execute("DELETE FROM settings")
        cursor.execute("DELETE FROM managers")
        cursor.execute("DELETE FROM companies")
        
        conn.commit()
        conn.close()
        
        print("Database reset complete")


def main():
    """Main function to generate company data"""
    print("DEVLENS COMPANY DATA GENERATOR")
    print("=" * 50)
    
    generator = CompanyDataGenerator(seed=42)
    
    # Option to reset database
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        generator.reset_database()
        print()
    
    # Generate companies
    success = generator.generate_all_companies()
    
    if success:
        print("\nNext steps:")
        print("1. Start backend: python backend/main.py")
        print("2. Login with any of these managers:")
        for template in generator.company_templates:
            mgr = template["manager"]
            print(f"   - {mgr['email']} / {mgr['password']} ({template['name']})")
        print("3. View your team's performance analytics!")
    else:
        print("\nSome companies may already exist. Use --reset to start fresh.")


if __name__ == "__main__":
    main()