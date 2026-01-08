import sqlite3
import json
import hashlib
from datetime import datetime

class DevLensDB:
    def __init__(self, db_path="devlens.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Companies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Managers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS managers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                company_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id)
            )
        ''')
        
        # Teams table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                company_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id)
            )
        ''')
        
        # Developers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS developers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                team_id INTEGER NOT NULL,
                company_id INTEGER NOT NULL,
                commits INTEGER DEFAULT 0,
                entropy REAL DEFAULT 0.0,
                meetings INTEGER DEFAULT 0,
                messages TEXT DEFAULT '[]',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id) REFERENCES teams (id),
                FOREIGN KEY (company_id) REFERENCES companies (id)
            )
        ''')
        
        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                manager_id INTEGER NOT NULL,
                email_address TEXT NOT NULL,
                email_alerts BOOLEAN DEFAULT 1,
                performance_alerts BOOLEAN DEFAULT 1,
                weekly_reports BOOLEAN DEFAULT 0,
                team_updates BOOLEAN DEFAULT 1,
                critical_issues BOOLEAN DEFAULT 1,
                settings_json TEXT DEFAULT '{}',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (manager_id) REFERENCES managers (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Insert initial data if tables are empty
        self.insert_initial_data()
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def insert_initial_data(self):
        """Insert initial companies, managers, teams, and developers"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM companies")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Insert companies
        companies = [
            "TechCorp Inc.",
            "Innovate Solutions", 
            "StartupIO"
        ]
        
        company_ids = {}
        for company in companies:
            cursor.execute("INSERT INTO companies (name) VALUES (?)", (company,))
            company_ids[company] = cursor.lastrowid
        
        # Insert managers
        managers = [
            {
                "email": "john.smith@techcorp.com",
                "password": "admin123",
                "name": "John Smith",
                "role": "Engineering Manager",
                "company": "TechCorp Inc."
            },
            {
                "email": "sarah.johnson@innovate.com", 
                "password": "manager456",
                "name": "Sarah Johnson",
                "role": "Development Director",
                "company": "Innovate Solutions"
            },
            {
                "email": "mike.chen@startup.io",
                "password": "startup789", 
                "name": "Mike Chen",
                "role": "CTO",
                "company": "StartupIO"
            }
        ]
        
        manager_ids = {}
        for manager in managers:
            password_hash = self.hash_password(manager["password"])
            cursor.execute('''
                INSERT INTO managers (email, password_hash, name, role, company_id) 
                VALUES (?, ?, ?, ?, ?)
            ''', (
                manager["email"],
                password_hash,
                manager["name"], 
                manager["role"],
                company_ids[manager["company"]]
            ))
            manager_ids[manager["email"]] = cursor.lastrowid
        
        # Insert teams
        teams_data = [
            {"name": "Backend", "company": "TechCorp Inc."},
            {"name": "Frontend", "company": "TechCorp Inc."},
            {"name": "DevOps", "company": "TechCorp Inc."},
            {"name": "Frontend", "company": "Innovate Solutions"},
            {"name": "QA", "company": "Innovate Solutions"},
            {"name": "Mobile", "company": "Innovate Solutions"},
            {"name": "Full Stack", "company": "StartupIO"},
            {"name": "Data Science", "company": "StartupIO"}
        ]
        
        team_ids = {}
        for team in teams_data:
            cursor.execute('''
                INSERT INTO teams (name, company_id) VALUES (?, ?)
            ''', (team["name"], company_ids[team["company"]]))
            team_key = f"{team['name']}_{team['company']}"
            team_ids[team_key] = cursor.lastrowid
        
        # Insert developers with more varied and realistic data
        developers_data = [
            # TechCorp Inc. - Traditional Enterprise (Conservative, Process-Heavy)
            {"name": "Alex", "team": "Backend", "company": "TechCorp Inc.", "commits": 14, "entropy": 0.95, "meetings": 2, "messages": ["Fixed memory leak in payment service", "Optimized database queries", "Security patch deployed"]},
            {"name": "Jordan", "team": "Frontend", "company": "TechCorp Inc.", "commits": 8, "entropy": 0.45, "meetings": 15, "messages": ["Daily standup notes", "UI review meeting", "Coordinating with design team", "Sprint planning discussion"]},
            {"name": "Sam", "team": "Backend", "company": "TechCorp Inc.", "commits": 22, "entropy": 0.88, "meetings": 6, "messages": ["Microservices architecture update", "API performance improvements", "Code review completed"]},
            {"name": "Taylor", "team": "Frontend", "company": "TechCorp Inc.", "commits": 6, "entropy": 0.35, "meetings": 12, "messages": ["Learning React patterns", "Component library updates", "Accessibility improvements"]},
            {"name": "Casey", "team": "DevOps", "company": "TechCorp Inc.", "commits": 16, "entropy": 0.92, "meetings": 3, "messages": ["CI/CD pipeline optimization", "Infrastructure as code", "Monitoring setup complete"]},
            {"name": "Morgan", "team": "Backend", "company": "TechCorp Inc.", "commits": 11, "entropy": 0.72, "meetings": 8, "messages": ["Database migration scripts", "API documentation", "Integration testing"]},
            {"name": "Riley", "team": "Frontend", "company": "TechCorp Inc.", "commits": 18, "entropy": 0.65, "meetings": 7, "messages": ["Component refactoring", "Performance optimization", "Cross-browser testing"]},
            {"name": "Avery", "team": "DevOps", "company": "TechCorp Inc.", "commits": 9, "entropy": 0.78, "meetings": 11, "messages": ["Infrastructure planning", "Security compliance", "Deployment automation"]},
            
            # Innovate Solutions - Modern Agile Startup (High Communication, Collaborative)
            {"name": "Emma", "team": "Frontend", "company": "Innovate Solutions", "commits": 25, "entropy": 0.92, "meetings": 4, "messages": ["React 18 migration complete", "New design system implementation", "Performance metrics improved by 40%"]},
            {"name": "Liam", "team": "QA", "company": "Innovate Solutions", "commits": 12, "entropy": 0.55, "meetings": 16, "messages": ["Test automation framework", "Bug triage meeting", "Quality metrics review", "Cross-team collaboration"]},
            {"name": "Sophia", "team": "Frontend", "company": "Innovate Solutions", "commits": 19, "entropy": 0.78, "meetings": 9, "messages": ["Mobile-first responsive design", "CSS-in-JS optimization", "User experience improvements"]},
            {"name": "Noah", "team": "Mobile", "company": "Innovate Solutions", "commits": 21, "entropy": 0.89, "meetings": 5, "messages": ["Flutter app performance tuning", "iOS deployment pipeline", "Native module integration"]},
            {"name": "Olivia", "team": "QA", "company": "Innovate Solutions", "commits": 7, "entropy": 0.42, "meetings": 18, "messages": ["Manual testing protocols", "User acceptance testing", "Quality assurance meetings", "Bug reporting system"]},
            {"name": "William", "team": "Mobile", "company": "Innovate Solutions", "commits": 17, "entropy": 0.83, "meetings": 8, "messages": ["React Native optimization", "App store deployment", "Cross-platform compatibility"]},
            {"name": "Charlotte", "team": "Frontend", "company": "Innovate Solutions", "commits": 13, "entropy": 0.68, "meetings": 11, "messages": ["Component library maintenance", "Design system updates", "Accessibility compliance"]},
            {"name": "Mason", "team": "QA", "company": "Innovate Solutions", "commits": 9, "entropy": 0.48, "meetings": 14, "messages": ["Automated testing suite", "Performance testing", "Quality gate reviews"]},
            
            # StartupIO - Lean Tech Startup (High Performance, Low Process)
            {"name": "Ava", "team": "Full Stack", "company": "StartupIO", "commits": 28, "entropy": 0.96, "meetings": 2, "messages": ["Full-stack feature shipped", "Database optimization complete", "System architecture redesign"]},
            {"name": "James", "team": "Data Science", "company": "StartupIO", "commits": 15, "entropy": 0.91, "meetings": 6, "messages": ["ML model deployment", "Data pipeline optimization", "Analytics dashboard v2.0"]},
            {"name": "Isabella", "team": "Full Stack", "company": "StartupIO", "commits": 24, "entropy": 0.87, "meetings": 4, "messages": ["API gateway implementation", "Real-time features", "Scalability improvements"]},
            {"name": "Benjamin", "team": "Data Science", "company": "StartupIO", "commits": 11, "entropy": 0.85, "meetings": 8, "messages": ["Statistical analysis complete", "Predictive model training", "Data visualization tools"]},
            {"name": "Mia", "team": "Full Stack", "company": "StartupIO", "commits": 26, "entropy": 0.94, "meetings": 3, "messages": ["Microservices architecture", "Performance monitoring", "Zero-downtime deployment"]},
            {"name": "Lucas", "team": "Data Science", "company": "StartupIO", "commits": 8, "entropy": 0.76, "meetings": 12, "messages": ["Research on new algorithms", "Data quality assessment", "Model validation"]},
            {"name": "Amelia", "team": "Full Stack", "company": "StartupIO", "commits": 20, "entropy": 0.82, "meetings": 5, "messages": ["Frontend optimization", "Backend API improvements", "Integration testing"]}
        ]
        
        for dev in developers_data:
            team_key = f"{dev['team']}_{dev['company']}"
            messages_json = json.dumps(dev["messages"])
            cursor.execute('''
                INSERT INTO developers (name, team_id, company_id, commits, entropy, meetings, messages)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                dev["name"],
                team_ids[team_key],
                company_ids[dev["company"]],
                dev["commits"],
                dev["entropy"],
                dev["meetings"],
                messages_json
            ))
        
        conn.commit()
        conn.close()
    
    def authenticate_manager(self, email, password_hash, company_name):
        """Authenticate manager login - expects pre-hashed password"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.id, m.email, m.name, m.role, c.name as company_name
            FROM managers m
            JOIN companies c ON m.company_id = c.id
            WHERE m.email = ? AND m.password_hash = ? AND c.name = ?
        ''', (email, password_hash, company_name))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "id": result[0],
                "email": result[1],
                "name": result[2],
                "role": result[3],
                "company": result[4]
            }
        return None
    
    def get_company_developers(self, company_name):
        """Get all developers for a specific company"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT d.name, t.name as team, d.commits, d.entropy, d.meetings, d.messages
            FROM developers d
            JOIN teams t ON d.team_id = t.id
            JOIN companies c ON d.company_id = c.id
            WHERE c.name = ?
        ''', (company_name,))
        
        results = cursor.fetchall()
        conn.close()
        
        developers = []
        for row in results:
            developers.append({
                "name": row[0],
                "team": row[1],
                "commits": row[2],
                "entropy": row[3],
                "meetings": row[4],
                "msgs": json.loads(row[5])
            })
        
        return developers
    
    def get_companies(self):
        """Get all companies"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name FROM companies ORDER BY name")
        results = cursor.fetchall()
        conn.close()
        
        return results  # Return tuples of (id, name)
    
    def get_manager_by_id(self, manager_id):
        """Get manager by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM managers WHERE id = ?", (manager_id,))
        result = cursor.fetchone()
        conn.close()
        
        return result
    
    def get_company_by_id(self, company_id):
        """Get company by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM companies WHERE id = ?", (company_id,))
        result = cursor.fetchone()
        conn.close()
        
        return result
    
    def create_company_and_manager(self, company_name, manager_email, manager_password, manager_name):
        """Create a new company and manager"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check if company already exists
            cursor.execute("SELECT id FROM companies WHERE name = ?", (company_name,))
            company_result = cursor.fetchone()
            
            if not company_result:
                # Create company
                cursor.execute("INSERT INTO companies (name) VALUES (?)", (company_name,))
                company_id = cursor.lastrowid
                is_new_company = True
            else:
                company_id = company_result[0]
                is_new_company = False
            
            # Create manager (password should already be hashed)
            cursor.execute('''
                INSERT INTO managers (email, password_hash, name, role, company_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (manager_email, manager_password, manager_name, "Manager", company_id))
            
            manager_id = cursor.lastrowid
            
            # If it's a new company, create sample teams and employees
            if is_new_company:
                self._create_sample_data_for_company(cursor, company_id, company_name)
            
            conn.commit()
            conn.close()
            
            # Create default email settings for the manager
            self.create_default_settings_for_manager(manager_id, manager_email)
            
            return manager_id
            
        except sqlite3.IntegrityError as e:
            conn.close()
            if "UNIQUE constraint failed" in str(e):
                raise Exception("UNIQUE constraint failed: managers.email")
            else:
                raise Exception("Registration failed")
        except Exception as e:
            conn.close()
            raise e
    
    def _create_sample_data_for_company(self, cursor, company_id, company_name):
        """Create sample teams and employees for a new company"""
        import random
        
        # Define possible teams
        team_options = [
            "Frontend", "Backend", "Full Stack", "DevOps", "QA", 
            "Mobile", "Data Science", "UI/UX", "Security", "Platform"
        ]
        
        # Create 3-4 random teams for the company
        num_teams = random.randint(3, 4)
        selected_teams = random.sample(team_options, num_teams)
        
        team_ids = {}
        for team_name in selected_teams:
            cursor.execute("INSERT INTO teams (name, company_id) VALUES (?, ?)", (team_name, company_id))
            team_ids[team_name] = cursor.lastrowid
        
        # Generate diverse employee names
        first_names = [
            "Alex", "Jordan", "Sam", "Taylor", "Casey", "Morgan", "Riley", "Avery",
            "Emma", "Liam", "Sophia", "Noah", "Olivia", "William", "Ava", "James",
            "Isabella", "Benjamin", "Mia", "Lucas", "Charlotte", "Mason", "Amelia",
            "Ethan", "Harper", "Alexander", "Evelyn", "Henry", "Abigail", "Sebastian"
        ]
        
        # Create 12-18 employees with varied performance profiles
        num_employees = random.randint(12, 18)
        used_names = set()
        
        for i in range(num_employees):
            # Generate unique name
            while True:
                name = random.choice(first_names)
                if name not in used_names:
                    used_names.add(name)
                    break
            
            # Assign to random team
            team_name = random.choice(selected_teams)
            team_id = team_ids[team_name]
            
            # Generate performance profile based on different archetypes
            archetype = random.choices([
                "high_performer",      # High commits, high complexity, low meetings
                "communicator",        # Moderate commits, low complexity, high meetings  
                "balanced",           # Moderate everything
                "specialist",         # High commits, high complexity, very low meetings (Hidden Gems)
                "junior",             # Low commits, low complexity, high meetings
                "senior_architect"    # High commits, very high complexity, very low meetings (Hidden Gems)
            ], weights=[20, 25, 30, 15, 5, 5])[0]  # Weighted selection
            
            if archetype == "high_performer":
                commits = random.randint(18, 25)
                entropy = random.uniform(0.8, 0.95)
                meetings = random.randint(1, 4)
                messages = [
                    f"Optimized {random.choice(['database', 'API', 'algorithm', 'performance'])}",
                    f"Implemented {random.choice(['new feature', 'security fix', 'optimization'])}",
                    f"Fixed critical {random.choice(['bug', 'memory leak', 'race condition'])}"
                ]
            elif archetype == "communicator":
                commits = random.randint(5, 12)
                entropy = random.uniform(0.3, 0.5)
                meetings = random.randint(12, 18)
                messages = [
                    "Great meeting today!",
                    "Let's sync up on this",
                    f"Coordinating with {random.choice(['design', 'product', 'QA'])} team",
                    "Status update ready",
                    "Thanks for the feedback",
                    "Looking forward to collaborating",
                    "Let me know if you need help"
                ]
            elif archetype == "balanced":
                commits = random.randint(10, 16)
                entropy = random.uniform(0.6, 0.8)
                meetings = random.randint(6, 10)
                messages = [
                    f"Working on {random.choice(['feature', 'bugfix', 'refactor'])}",
                    "Code review completed",
                    f"Testing {random.choice(['integration', 'unit tests', 'deployment'])}"
                ]
            elif archetype == "specialist":
                commits = random.randint(15, 22)  # High commits
                entropy = random.uniform(0.85, 0.98)  # High complexity
                meetings = random.randint(1, 3)  # Very low meetings
                messages = [
                    f"Deep dive into {random.choice(['architecture', 'algorithms', 'performance'])}",
                    f"Research on {random.choice(['new technology', 'optimization', 'security'])}"
                    # Fewer messages = low visibility
                ]
            elif archetype == "junior":
                commits = random.randint(3, 8)
                entropy = random.uniform(0.2, 0.4)
                meetings = random.randint(8, 15)
                messages = [
                    "Learning the codebase",
                    "Need help with setup",
                    f"Working on {random.choice(['documentation', 'simple feature', 'bug fix'])}",
                    "Thanks for the guidance!",
                    "Can someone help me with this?",
                    "Still figuring this out"
                ]
            else:  # senior_architect
                commits = random.randint(12, 18)  # High commits
                entropy = random.uniform(0.9, 0.98)  # Very high complexity
                meetings = random.randint(1, 2)  # Very low meetings
                messages = [
                    f"Architecting {random.choice(['microservices', 'data pipeline', 'system design'])}",
                    f"Technical decision on {random.choice(['framework', 'database', 'infrastructure'])}"
                    # Minimal messages = low visibility despite high impact
                ]
            
            # Add some randomness to make it more realistic
            commits += random.randint(-2, 3)
            entropy += random.uniform(-0.1, 0.1)
            meetings += random.randint(-2, 3)
            
            # Ensure values are within bounds
            commits = max(0, commits)
            entropy = max(0.1, min(1.0, entropy))
            meetings = max(0, meetings)
            
            # Insert employee
            messages_json = json.dumps(messages)
            cursor.execute('''
                INSERT INTO developers (name, team_id, company_id, commits, entropy, meetings, messages)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, team_id, company_id, commits, entropy, meetings, messages_json))
    
    def add_developer(self, name, team_name, company_name, commits=0, entropy=0.0, meetings=0, messages=None):
        """Add a new developer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if messages is None:
            messages = []
        
        try:
            # Get company ID
            cursor.execute("SELECT id FROM companies WHERE name = ?", (company_name,))
            company_id = cursor.fetchone()[0]
            
            # Get or create team
            cursor.execute("SELECT id FROM teams WHERE name = ? AND company_id = ?", (team_name, company_id))
            team_result = cursor.fetchone()
            
            if not team_result:
                cursor.execute("INSERT INTO teams (name, company_id) VALUES (?, ?)", (team_name, company_id))
                team_id = cursor.lastrowid
            else:
                team_id = team_result[0]
            
            # Add developer
            messages_json = json.dumps(messages)
            cursor.execute('''
                INSERT INTO developers (name, team_id, company_id, commits, entropy, meetings, messages)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, team_id, company_id, commits, entropy, meetings, messages_json))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            conn.close()
            return False
    
    def get_manager_settings(self, manager_id):
        """Get manager's email settings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check if the new columns exist
            cursor.execute("PRAGMA table_info(settings)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'email_address' in columns:
                # New schema with email columns
                cursor.execute('''
                    SELECT email_address, email_alerts, performance_alerts, weekly_reports, 
                           team_updates, critical_issues, settings_json
                    FROM settings WHERE manager_id = ?
                ''', (manager_id,))
                
                result = cursor.fetchone()
                
                if result:
                    return {
                        'email_address': result[0],
                        'email_alerts': bool(result[1]),
                        'performance_alerts': bool(result[2]),
                        'weekly_reports': bool(result[3]),
                        'team_updates': bool(result[4]),
                        'critical_issues': bool(result[5]),
                        'settings_json': result[6]
                    }
            else:
                # Old schema - get manager email as default
                cursor.execute('''
                    SELECT m.email FROM managers m WHERE m.id = ?
                ''', (manager_id,))
                
                manager_result = cursor.fetchone()
                if manager_result:
                    return {
                        'email_address': manager_result[0],
                        'email_alerts': True,
                        'performance_alerts': True,
                        'weekly_reports': False,
                        'team_updates': True,
                        'critical_issues': True,
                        'settings_json': '{}'
                    }
            
        except Exception as e:
            print(f"Error getting manager settings: {str(e)}")
        finally:
            conn.close()
        
        return None
    
    def update_manager_settings(self, manager_id, email_address, email_alerts=True, 
                              performance_alerts=True, weekly_reports=False, 
                              team_updates=True, critical_issues=True, settings_json='{}'):
        """Update manager's email settings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check if the new columns exist
            cursor.execute("PRAGMA table_info(settings)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'email_address' not in columns:
                # Need to migrate database first
                print("⚠️  Database needs migration. Please run: python migrate_database.py")
                return False
            
            # Check if settings exist
            cursor.execute("SELECT id FROM settings WHERE manager_id = ?", (manager_id,))
            exists = cursor.fetchone()
            
            if exists:
                # Update existing settings
                cursor.execute('''
                    UPDATE settings SET 
                        email_address = ?, email_alerts = ?, performance_alerts = ?,
                        weekly_reports = ?, team_updates = ?, critical_issues = ?,
                        settings_json = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE manager_id = ?
                ''', (email_address, email_alerts, performance_alerts, weekly_reports,
                      team_updates, critical_issues, settings_json, manager_id))
            else:
                # Insert new settings
                cursor.execute('''
                    INSERT INTO settings (manager_id, email_address, email_alerts, 
                                        performance_alerts, weekly_reports, team_updates, 
                                        critical_issues, settings_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (manager_id, email_address, email_alerts, performance_alerts,
                      weekly_reports, team_updates, critical_issues, settings_json))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error updating manager settings: {str(e)}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def create_default_settings_for_manager(self, manager_id, manager_email):
        """Create default settings for a new manager"""
        return self.update_manager_settings(
            manager_id=manager_id,
            email_address=manager_email,
            email_alerts=True,
            performance_alerts=True,
            weekly_reports=False,
            team_updates=True,
            critical_issues=True
        )