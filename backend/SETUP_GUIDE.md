# 🚀 DevLens Complete Setup Guide

## Quick Start (5 minutes)

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://127.0.0.1:8000

## 🔧 Database Setup (Automatic)

The database is automatically created and migrated when you start the backend:

1. **New Installation**: Creates fresh database with sample data
2. **Existing Database**: Automatically migrates to add email features
3. **Missing Settings**: Creates default email settings for existing managers

### Manual Database Operations

```bash
# Check database structure
python check_db.py

# Migrate existing database
python migrate_database.py

# Fix existing managers (create default settings)
python fix_existing_managers.py

# Interactive manager creation
python create_manager.py
```

## 📧 Email System Setup

### Demo Mode (Default)
- **No configuration needed**
- Emails are printed to backend console
- Perfect for testing and development

### Production Mode (Real Emails)

1. **Update email_service.py**:
   ```python
   # Add your SMTP credentials
   self.sender_email = "your-email@gmail.com"
   self.sender_password = "your-app-password"
   
   # Uncomment these lines in send_email method:
   server.login(self.sender_email, self.sender_password)
   server.sendmail(self.sender_email, to_email, message.as_string())
   ```

2. **Gmail Setup** (Recommended):
   - Enable 2-Factor Authentication
   - Generate App Password: Google Account → Security → App passwords
   - Use app password (not account password)

## 🎯 Testing Email Features

### 1. Login to DevLens
- Use demo credentials or create new account
- **TechCorp**: john.smith@techcorp.com / admin123
- **Innovate**: sarah.johnson@innovate.com / manager456
- **StartupIO**: mike.chen@startup.io / startup789

### 2. Configure Email Settings
- Go to Settings → Notifications
- Email defaults to your login email
- Toggle notification types on/off
- Click "Test Email" to verify setup

### 3. Send Sample Emails
- **Test Email**: Verify configuration
- **Performance Alert**: Sample performance notification
- **Weekly Report**: Comprehensive team analytics
- **Critical Issues**: Urgent performance alerts

### 4. Check Backend Console
In demo mode, you'll see email content printed like:
```
📧 EMAIL SENT TO: john.smith@techcorp.com
📧 SUBJECT: ✅ DevLens Email Test - Configuration Successful
📧 CONTENT: <html>...
```

## 🏢 Multi-Company Features

### Create New Company & Manager
1. **Frontend Registration**:
   - Click "Create New Company & Manager Account"
   - Fill out company and manager details
   - System auto-generates 12-18 diverse employees

2. **Backend Registration**:
   ```bash
   python create_manager.py
   ```

### Company Profiles
Each company has distinct characteristics:
- **TechCorp Inc.**: Traditional enterprise (process-heavy)
- **Innovate Solutions**: Modern agile startup (high collaboration)
- **StartupIO**: Lean tech startup (high performance)

## 📊 Email Content Features

### Professional Templates
- **HTML formatted** with DevLens branding
- **Responsive design** for mobile/desktop
- **Rich content** with metrics and charts
- **Actionable insights** with recommendations

### Dynamic Content
- **Real performance data** from your teams
- **Team-specific metrics** and comparisons
- **Personalized recommendations** based on data
- **Direct dashboard links** for immediate action

### Email Types
1. **Test Email**: Configuration verification
2. **Performance Alerts**: Significant metric changes
3. **Weekly Reports**: Comprehensive team analytics
4. **Critical Issues**: Urgent performance problems
5. **Team Updates**: Member changes and updates

## 🔒 Security & Privacy

### Data Security
- **Password hashing** with SHA256
- **Company isolation** (managers only see own data)
- **Input validation** on all endpoints
- **TLS encryption** for email transmission

### Email Security
- **App passwords** recommended over account passwords
- **SMTP over TLS** for secure transmission
- **No credentials stored** in plain text

## 🐛 Troubleshooting

### Common Issues

1. **"500 Internal Server Error"**
   ```bash
   # Run database migration
   python migrate_database.py
   
   # Fix existing managers
   python fix_existing_managers.py
   ```

2. **"Email not working"**
   - Check backend console for demo output
   - Verify SMTP credentials for production
   - Check spam folder for real emails

3. **"No data showing"**
   - Ensure backend is running on port 8000
   - Check browser console for API errors
   - Verify company has developers

### Debug Commands
```bash
# Check database structure
python check_db.py

# Test API endpoints
curl http://127.0.0.1:8000/api/companies
curl http://127.0.0.1:8000/api/settings/1

# View backend logs
python main.py  # Watch console output
```

## 🚀 Production Deployment

### Environment Variables
```bash
# Email configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password

# Database
DATABASE_URL=sqlite:///devlens.db

# Security
SECRET_KEY=your-secret-key
```

### Docker Deployment
```dockerfile
# Dockerfile example
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📈 Next Steps

### Immediate Use
1. ✅ Login with demo credentials
2. ✅ Test email notifications
3. ✅ Explore team analytics
4. ✅ Create new companies/managers

### Customization
1. 🔧 Add your SMTP credentials for real emails
2. 🎨 Customize email templates
3. 📊 Add more performance metrics
4. 🔄 Set up automated scheduling

### Advanced Features
1. 📅 Scheduled weekly reports
2. 🚨 Real-time performance monitoring
3. 📱 Mobile app integration
4. 🤖 AI-powered insights

---

**Need help?** Check the console output, run debug scripts, or review the API documentation at http://127.0.0.1:8000/docs 🚀