#!/usr/bin/env python3
"""
Test email sending functionality
"""

from email_service import EmailService

def test_email_sending():
    print("🧪 Testing Email Configuration")
    print("=" * 50)
    
    # Create email service
    email_service = EmailService()
    
    print(f"📧 Sender Email: {email_service.sender_email}")
    print(f"🌐 SMTP Server: {email_service.smtp_server}:{email_service.port}")
    
    # Get recipient email
    recipient = input("\n📮 Enter recipient email address: ").strip()
    
    if not recipient:
        print("❌ No recipient email provided!")
        return
    
    # Test email content
    subject = "🧪 DevLens Email Test"
    html_content = """
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #16a34a;">✅ Email Test Successful!</h2>
        <p>This is a test email from DevLens Analytics.</p>
        <p>If you received this email, your email configuration is working correctly!</p>
        <hr>
        <p style="font-size: 12px; color: #666;">
            Sent from DevLens Analytics System
        </p>
    </body>
    </html>
    """
    
    print(f"\n🚀 Sending test email to: {recipient}")
    print("-" * 30)
    
    # Send email
    success = email_service.send_email(recipient, subject, html_content)
    
    if success:
        print("\n🎉 Email sent successfully!")
        print("📬 Check your inbox (and spam folder)")
    else:
        print("\n❌ Email sending failed!")
        print("\n🔧 Troubleshooting Steps:")
        print("1. Check your Gmail App Password setup")
        print("2. Verify 2-Factor Authentication is enabled")
        print("3. Make sure 'Less secure app access' is disabled (use App Password instead)")
        print("4. Check your internet connection")

def gmail_setup_guide():
    print("\n📧 Gmail App Password Setup Guide")
    print("=" * 40)
    print("1. Go to your Google Account settings")
    print("2. Navigate to Security → 2-Step Verification")
    print("3. Enable 2-Step Verification if not already enabled")
    print("4. Go to Security → App passwords")
    print("5. Select 'Mail' and generate a password")
    print("6. Use this 16-character password in email_service.py")
    print("\n⚠️  Important: Use the App Password, NOT your regular Gmail password!")

if __name__ == "__main__":
    print("DevLens Email Testing Tool")
    print("=" * 30)
    
    choice = input("Choose option:\n1. Test email sending\n2. Gmail setup guide\n3. Both\nEnter (1/2/3): ").strip()
    
    if choice in ['2', '3']:
        gmail_setup_guide()
    
    if choice in ['1', '3']:
        test_email_sending()