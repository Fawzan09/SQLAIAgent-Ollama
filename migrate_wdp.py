#!/usr/bin/env python3
"""
WDP Database Migration Script
This script helps you integrate your WDP project database with the SQL AI Agent.
"""

import os
import sqlite3
import shutil
from pathlib import Path

def migrate_wdp_database():
    """
    Instructions for migrating your WDP database to work with the SQL AI Agent.
    """
    
    print("🏢 WDP Database Migration Guide")
    print("=" * 50)
    
    print("\n📋 STEP 1: Locate Your WDP Database")
    print("   • Find your WDP project database file (usually .db, .sqlite, or .sqlite3)")
    print("   • Common locations: ./database/, ./db/, ./data/, or project root")
    
    print("\n📋 STEP 2: Copy Database to SQL AI Agent")
    print("   • Copy your database file to this directory")
    print("   • Rename it to 'wdp_office.db' for clarity")
    
    print("\n📋 STEP 3: Update Environment Configuration")
    print("   • Update the DB_URL in your .env file:")
    print("   • For SQLite: DB_URL=sqlite:///./wdp_office.db")
    print("   • For PostgreSQL: DB_URL=postgresql://user:pass@localhost/wdp_db")
    print("   • For MySQL: DB_URL=mysql://user:pass@localhost/wdp_db")
    
    print("\n📋 STEP 4: Test the Connection")
    print("   • Run the application: chainlit run app.py")
    print("   • Try commands like '/schema' and '/tables'")
    
    print("\n🔧 AUTOMATED MIGRATION (if you have the WDP database file)")
    
    # Look for potential database files
    current_dir = Path(".")
    db_files = []
    
    for pattern in ["*.db", "*.sqlite", "*.sqlite3"]:
        db_files.extend(current_dir.glob(pattern))
    
    if db_files:
        print(f"\n📁 Found potential database files:")
        for i, db_file in enumerate(db_files, 1):
            print(f"   {i}. {db_file}")
        
        try:
            choice = input(f"\nSelect database file to use (1-{len(db_files)}) or 'n' to skip: ")
            if choice.isdigit() and 1 <= int(choice) <= len(db_files):
                selected_db = db_files[int(choice) - 1]
                backup_existing_db()
                shutil.copy2(selected_db, "wdp_office.db")
                update_env_file()
                print(f"✅ Successfully migrated {selected_db} to wdp_office.db")
                test_database_connection()
            else:
                print("⏭️  Skipping automated migration")
        except (ValueError, KeyboardInterrupt):
            print("⏭️  Skipping automated migration")
    else:
        print("\n❌ No database files found in current directory")
    
    print("\n🎯 MANUAL MIGRATION STEPS:")
    print("1. Place your WDP database file in this directory")
    print("2. Update .env file with correct DB_URL")
    print("3. Run: chainlit run app.py")
    print("4. Test with: /schema command")

def backup_existing_db():
    """Backup existing database if it exists"""
    if os.path.exists("example.db"):
        shutil.copy2("example.db", "example.db.backup")
        print("📦 Backed up existing example.db to example.db.backup")

def update_env_file():
    """Update .env file with new database URL"""
    env_content = ""
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            env_content = f.read()
    
    # Update or add DB_URL
    lines = env_content.split('\n')
    db_url_updated = False
    
    for i, line in enumerate(lines):
        if line.startswith("DB_URL="):
            lines[i] = "DB_URL=sqlite:///./wdp_office.db"
            db_url_updated = True
            break
    
    if not db_url_updated:
        lines.append("DB_URL=sqlite:///./wdp_office.db")
    
    with open(".env", "w") as f:
        f.write('\n'.join(lines))
    
    print("🔧 Updated .env file with new database URL")

def test_database_connection():
    """Test the database connection"""
    try:
        conn = sqlite3.connect("wdp_office.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n✅ Database connection successful!")
        print(f"📊 Found {len(tables)} tables:")
        for table in tables:
            print(f"   • {table[0]}")
        
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Database connection failed: {e}")
        print("   Please check your database file and try again.")

if __name__ == "__main__":
    migrate_wdp_database()
