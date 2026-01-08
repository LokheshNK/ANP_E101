#!/usr/bin/env python3
"""
Gmail setup checker and troubleshooter
"""

import smtplib
import ssl
from email_service import EmailService

def check_gmail_setup():
    print("🔍 Gmail Setup Checker")
    print("=" * 30)
    
    email_service = EmailService()
    
    print(f"📧 Email: {email_service.sender_email}")
    print(f"🔑 Password: {'*' * len(email_service.sender_password)} ({len(email_service.sender_password)} characters)")
    
    # Check if it looks like an App Password (16 characters, no special chars)
    password = email_service.sender_password
    
    if len(password) == 16 and password.replace(' ', '').isalnum():
        print("✅ Password format looks like a Gmail App Password")
    else:
        print("⚠️  Password doesn't look like a Gmail App Password")
        print("   Gmail App Passwords are 16 characters (letters/numbers only)")
        print("   Example: 'abcd efgh ijkl mnop' or 'abcdefghijklmnop'")
    
    print(f"\n🌐 SMTP Server: {email_service.smtp_server}:{email_service.port}")
    
    # Test connection
    print("\n🔄 Testing SMTP connection...")
    
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(email_service.smtp_server, email_service.port) as server:
            print("✅ Connected to SMTP server")
            
            server.starttls(context=context)
            print("✅ TLS encryption enabled")
            
            server.login(email_service.sender_email, email_service.sender_password)
            print("✅ Authentication successful!")
            
            print("\n🎉 Gmail setup is working correctly!")
            return True
            
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("\n🔧 Fix this by:")
        print("1. Enable 2-Factor Authentication on your Gmail")
        print("2. Generate an App Password:")
        print("   • Go to Google Account → Security → App passwords")
        print("   • Select 'Mail' and generate password")
        print("   • Use the 16-character password (not your regular password)")
        return False
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("\n🔧 Check:")
        print("1. Internet connection")
        print("2. Gmail SMTP settings")
        print("3. Firewall/antivirus blocking SMTP")
        return False

def interactive_setup():
    print("\n🛠️  Interactive Gmail Setup")
    print("=" * 30)
    
    email = input("Enter your Gmail address: ").strip()
    password = input("Enter your Gmail App Password: ").strip()
    
    if not email.endswith('@gmail.com'):
        print("⚠️  Make sure you're using a Gmail address (@gmail.com)")
    
    if len(password) != 16:
        print("⚠️  Gmail App Passwords are exactly 16 characters")
        print("   If you have spaces, remove them: 'abcd efgh ijkl mnop' → 'abcdefghijklmnop'")
    
    print(f"\n📝 Update your email_service.py with:")
    print(f'self.sender_email = "{email}"')
    print(f'self.sender_password = "{password}"')
    
    # Test the new credentials
    print("\n🧪 Testing new credentials...")
    
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(email, password)
            print("✅ New credentials work!")
            
    except Exception as e:
        print(f"❌ New credentials failed: {e}")

if __name__ == "__main__":
    print("Gmail Setup Checker for DevLens")
    print("=" * 35)
    
    choice = input("Choose option:\n1. Check current setup\n2. Interactive setup\n3. Both\nEnter (1/2/3): ").strip()
    
    if choice in ['1', '3']:
        success = check_gmail_setup()
        if not success and choice == '3':
            print("\n" + "="*50)
    
    if choice in ['2', '3']:
        interactive_setup()