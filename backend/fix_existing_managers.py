#!/usr/bin/env python3
"""
Create default settings for existing managers
"""

import sqlite3
import os

def fix_existing_managers():
    db_path = "devlens.db"
    
    if not os.path.exists(db_path):
        print("❌ Database doesn't exist!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("🔧 Creating default settings for existing managers...")
        
        # Get all managers without settings
        cursor.execute('''
            SELECT m.id, m.email, m.name 
            FROM managers m 
            LEFT JOIN settings s ON m.id = s.manager_id 
            WHERE s.manager_id IS NULL
        ''')
        
        managers_without_settings = cursor.fetchall()
        
        if not managers_without_settings:
            print("✅ All managers already have settings!")
            return
        
        print(f"📝 Found {len(managers_without_settings)} managers without settings:")
        
        for manager_id, email, name in managers_without_settings:
            print(f"   • {name} ({email})")
            
            # Create default settings
            cursor.execute('''
                INSERT INTO settings (
                    manager_id, email_address, email_alerts, performance_alerts,
                    weekly_reports, team_updates, critical_issues, settings_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (manager_id, email, True, True, False, True, True, '{}'))
        
        conn.commit()
        print(f"✅ Created default settings for {len(managers_without_settings)} managers!")
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM settings")
        total_settings = cursor.fetchone()[0]
        print(f"📊 Total settings records: {total_settings}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_existing_managers()