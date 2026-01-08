# DevLens Email Setup Guide

DevLens now supports real email notifications for performance alerts, weekly reports, and critical issues.

## 🚀 Quick Start (Demo Mode)

The system is currently configured in **demo mode** - emails are simulated and printed to the console instead of being sent. This allows you to test all functionality without email server setup.

### Testing Email Features:

1. **Start the backend:**
   ```bash
   cd backend
   python main.py
   ```

2. **Go to Settings in the frontend**
3. **Configure your email address** (defaults to login email)
4. **Click "Send Test Email"** - you'll see the email content in the backend console
5. **Try different email types** (Performance Alert, Weekly Report, etc.)

## 📧 Enable Real Email Sending

To send actual emails, you need to configure SMTP settings:

### Option 1: Gmail (Recommended for testing)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password:**
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"

3. **Update email_service.py:**
   ```python
   self.sender_email = "your-email@gmail.com"
   self.sender_password = "your-app-password"
   ```

4. **Uncomment the actual sending code** in `email_service.py`:
   ```python
   # Uncomment these lines:
   server.login(self.sender_email, self.sender_password)
   server.sendmail(self.sender_email, to_email, message.as_string())
   
   # Comment out the demo print statements
   ```

### Option 2: Other Email Providers

Update the SMTP configuration in `email_service.py`:

```python
# For Outlook/Hotmail
self.smtp_server = "smtp-mail.outlook.com"
self.port = 587

# For Yahoo
self.smtp_server = "smtp.mail.yahoo.com"
self.port = 587

# For custom SMTP
self.smtp_server = "your-smtp-server.com"
self.port = 587  # or 465 for SSL
```

## 📊 Email Types & Content

### 1. Test Email ✅
- **Purpose:** Verify email configuration
- **Content:** Welcome message with feature overview
- **Trigger:** Manual from settings

### 2. Performance Alerts 🚨
- **Purpose:** Notify about significant performance changes
- **Content:** 
  - Top performers list
  - Developers needing attention
  - Actionable recommendations
- **Trigger:** Manual or automated (when implemented)

### 3. Weekly Reports 📊
- **Purpose:** Comprehensive team performance summary
- **Content:**
  - Team metrics (commits, complexity, meetings)
  - Team-by-team breakdown
  - Key insights and trends
- **Trigger:** Manual or scheduled (when implemented)

### 4. Critical Issues 🚨
- **Purpose:** Immediate alerts for urgent issues
- **Content:**
  - Critical performance problems
  - Developers with zero commits
  - Excessive meeting loads
  - Immediate action items
- **Trigger:** Manual or real-time monitoring

## 🔧 Email Settings Features

### Default Email Address
- **Automatically uses login email** as default
- **Editable** - can change to any email address
- **Persistent** - saved in database per manager

### Notification Controls
- **Individual toggles** for each email type
- **Send Sample** buttons to preview content
- **Real-time testing** with actual data

### Professional Email Design
- **HTML formatted** emails with professional styling
- **Responsive design** works on mobile and desktop
- **Branded** with DevLens styling and colors
- **Actionable** with direct links to dashboard

## 🛡️ Security & Privacy

### Email Security
- **App passwords** recommended over account passwords
- **TLS encryption** for all email transmission
- **No sensitive data** stored in plain text

### Data Privacy
- **Manager isolation** - only see own company data
- **Configurable retention** - control how long data is kept
- **Opt-out options** - disable any notification type

## 🔄 Automation (Future Enhancement)

The current system supports manual email sending. Future versions can include:

- **Scheduled weekly reports** (cron jobs)
- **Real-time performance monitoring** with automatic alerts
- **Threshold-based notifications** (e.g., when commits drop below X)
- **Team milestone celebrations** (automated congratulations)

## 🐛 Troubleshooting

### Common Issues:

1. **"Authentication failed"**
   - Check email/password credentials
   - Ensure 2FA and app password for Gmail
   - Verify SMTP server settings

2. **"Connection refused"**
   - Check SMTP server and port
   - Verify firewall settings
   - Try different ports (587, 465, 25)

3. **"Email not received"**
   - Check spam/junk folder
   - Verify recipient email address
   - Check email provider limits

### Debug Mode:
The system currently runs in debug mode, printing all email content to console. This helps verify:
- Email content generation
- Data processing
- Template rendering
- API connectivity

## 📈 Usage Analytics

Track email engagement through:
- **Send success rates** (logged in backend)
- **Manager preferences** (stored in database)
- **Feature usage** (which email types are most used)

---

**Ready to test?** Start the backend, go to Settings → Notifications, and click "Send Test Email"! 🚀