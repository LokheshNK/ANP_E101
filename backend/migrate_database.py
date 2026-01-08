#!/usr/bin/env python3
"""
Database migration script to add email settings columns
"""

import sqlite3
import os

def migrate_database():
    db_path = "devlens.db"
    
    if not os.path.exists(db_path):
        print("Database doesn't exist. Creating new database with updated schema...")
        from database import DevLensDB
        db = DevLensDB()
        print("✅ New database created successfully!")
        return
    
    print("🔄 Migrating existing database...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if email_address column exists
        cursor.execute("PRAGMA table_info(settings)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'email_address' not in columns:
            print("📧 Adding email settings columns...")
            
            # Add new columns to settings table
            cursor.execute("ALTER TABLE settings ADD COLUMN email_address TEXT DEFAULT ''")
            cursor.execute("ALTER TABLE settings ADD COLUMN email_alerts BOOLEAN DEFAULT 1")
            cursor.execute("ALTER TABLE settings ADD COLUMN performance_alerts BOOLEAN DEFAULT 1")
            cursor.execute("ALTER TABLE settings ADD COLUMN weekly_reports BOOLEAN DEFAULT 0")
            cursor.execute("ALTER TABLE settings ADD COLUMN team_updates BOOLEAN DEFAULT 1")
            cursor.execute("ALTER TABLE settings ADD COLUMN critical_issues BOOLEAN DEFAULT 1")
            
            print("✅ Email settings columns added successfully!")
            
            # Update existing settings with manager emails
            cursor.execute('''
                UPDATE settings 
                SET email_address = (
                    SELECT email FROM managers WHERE managers.id = settings.manager_id
                )
                WHERE email_address = '' OR email_address IS NULL
            ''')
            
            print("✅ Default email addresses set from manager accounts!")
            
        else:
            print("✅ Database already has email settings columns!")
        
        conn.commit()
        print("🎉 Database migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()