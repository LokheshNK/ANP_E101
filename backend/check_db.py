#!/usr/bin/env python3
"""
Check database structure
"""

import sqlite3
import os

def check_database():
    db_path = "devlens.db"
    
    if not os.path.exists(db_path):
        print("❌ Database doesn't exist!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("📊 Database Structure:")
        print("=" * 50)
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"\n🗂️  Table: {table_name}")
            
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            for column in columns:
                col_id, col_name, col_type, not_null, default_val, pk = column
                print(f"   • {col_name} ({col_type})")
        
        print("\n" + "=" * 50)
        
        # Check settings table specifically
        print("\n🔍 Settings Table Details:")
        cursor.execute("PRAGMA table_info(settings)")
        settings_columns = cursor.fetchall()
        
        column_names = [col[1] for col in settings_columns]
        print(f"Columns: {column_names}")
        
        if 'email_address' in column_names:
            print("✅ Email columns exist!")
        else:
            print("❌ Email columns missing!")
        
        # Check if there are any settings records
        cursor.execute("SELECT COUNT(*) FROM settings")
        count = cursor.fetchone()[0]
        print(f"Settings records: {count}")
        
        if count > 0:
            cursor.execute("SELECT * FROM settings LIMIT 3")
            records = cursor.fetchall()
            print("Sample records:")
            for record in records:
                print(f"  {record}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_database()