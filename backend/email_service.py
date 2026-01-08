import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import json
from typing import List, Dict, Any

class EmailService:
    def __init__(self):
        # Gmail SMTP configuration (you can change this to other providers)
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
        
        # IMPORTANT: Replace with your Gmail App Password (16 characters)
        # Get this from: Google Account → Security → App passwords → Mail
        self.sender_email = "lokheshnk@gmail.com"
        self.sender_password = "ooop cgzt rxoy iixu"  # Replace with your actual App Password
        
    def send_email(self, to_email: str, subject: str, html_content: str, text_content: str = None):
        """Send an email with HTML content"""
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"DevLens Analytics <{self.sender_email}>"
            message["To"] = to_email
            
            # Create text and HTML parts
            if text_content:
                text_part = MIMEText(text_content, "plain")
                message.attach(text_part)
            
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Create secure connection and send email
            context = ssl.create_default_context()
            
            print(f"🔄 Attempting to send email to: {to_email}")
            print(f"📧 Using SMTP server: {self.smtp_server}:{self.port}")
            print(f"📤 From: {self.sender_email}")
            
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                print("🔐 Starting TLS...")
                server.starttls(context=context)
                
                print("� LSogging in...")
                server.login(self.sender_email, self.sender_password)
                
                print("📨 Sending email...")
                server.sendmail(self.sender_email, to_email, message.as_string())
                
                print(f"✅ EMAIL SENT SUCCESSFULLY TO: {to_email}")
                print(f"📧 SUBJECT: {subject}")
                
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ Authentication Error: {str(e)}")
            print("💡 Tips:")
            print("   1. Make sure you're using an App Password (not your regular Gmail password)")
            print("   2. Enable 2-Factor Authentication on your Gmail account")
            print("   3. Generate App Password: Google Account → Security → App passwords")
            return False
            
        except smtplib.SMTPRecipientsRefused as e:
            print(f"❌ Recipient Error: {str(e)}")
            print("💡 Check the recipient email address is valid")
            return False
            
        except smtplib.SMTPServerDisconnected as e:
            print(f"❌ Server Connection Error: {str(e)}")
            print("💡 Check your internet connection and SMTP settings")
            return False
            
        except Exception as e:
            print(f"❌ Unexpected Error: {str(e)}")
            print(f"❌ Error Type: {type(e).__name__}")
            return False
    
    def generate_performance_alert_email(self, manager_name: str, company: str, developers: List[Dict], alert_type: str):
        """Generate performance alert email content"""
        
        if alert_type == "performance_change":
            subject = f"🚨 Performance Alert - {company}"
            
            # Find developers with significant changes (simulated)
            high_performers = [d for d in developers if d.get('imp_z', 0) > 1.5]
            low_performers = [d for d in developers if d.get('imp_z', 0) < -0.5]
            
            html_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .header {{ background-color: #16a34a; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .alert {{ background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin: 15px 0; }}
                    .metric {{ background-color: #f3f4f6; padding: 10px; margin: 10px 0; border-radius: 5px; }}
                    .high-performer {{ color: #16a34a; font-weight: bold; }}
                    .low-performer {{ color: #dc2626; font-weight: bold; }}
                    .footer {{ background-color: #f9fafb; padding: 15px; text-align: center; font-size: 12px; color: #6b7280; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🛡️ DevLens Performance Alert</h1>
                    <p>Performance insights for {company}</p>
                </div>
                
                <div class="content">
                    <p>Hello {manager_name},</p>
                    
                    <div class="alert">
                        <strong>⚠️ Performance Alert Triggered</strong><br>
                        We've detected significant performance changes in your team that require attention.
                    </div>
                    
                    <h3>📊 Key Metrics Summary</h3>
                    <div class="metric">
                        <strong>Total Developers:</strong> {len(developers)}<br>
                        <strong>High Performers:</strong> <span class="high-performer">{len(high_performers)} developers</span><br>
                        <strong>Needs Attention:</strong> <span class="low-performer">{len(low_performers)} developers</span>
                    </div>
                    
                    <h3>🏆 Top Performers This Week</h3>
                    <ul>
            """
            
            # Add top performers
            top_performers = sorted(developers, key=lambda x: x.get('commits', 0), reverse=True)[:3]
            for dev in top_performers:
                html_content += f"""
                        <li><strong>{dev['name']}</strong> ({dev['team']}) - {dev['commits']} commits, {dev['entropy']:.2f} complexity</li>
                """
            
            html_content += """
                    </ul>
                    
                    <h3>📈 Recommendations</h3>
                    <ul>
                        <li>Schedule 1:1s with developers showing performance changes</li>
                        <li>Review workload distribution across teams</li>
                        <li>Consider pair programming for knowledge sharing</li>
                        <li>Celebrate high performers and share best practices</li>
                    </ul>
                    
                    <p>
                        <a href="http://localhost:3000" style="background-color: #16a34a; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                            View Full Dashboard
                        </a>
                    </p>
                </div>
                
                <div class="footer">
                    <p>This is an automated alert from DevLens Analytics. You can manage your notification preferences in the dashboard settings.</p>
                </div>
            </body>
            </html>
            """
            
        elif alert_type == "weekly_report":
            subject = f"📊 Weekly Team Report - {company}"
            
            # Calculate weekly metrics
            total_commits = sum(d.get('commits', 0) for d in developers)
            avg_complexity = sum(d.get('entropy', 0) for d in developers) / len(developers) if developers else 0
            total_meetings = sum(d.get('meetings', 0) for d in developers)
            
            # Group by teams
            teams = {}
            for dev in developers:
                team = dev.get('team', 'Unknown')
                if team not in teams:
                    teams[team] = []
                teams[team].append(dev)
            
            html_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .header {{ background-color: #16a34a; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .summary {{ background-color: #f0f9ff; border: 1px solid #0ea5e9; padding: 15px; margin: 15px 0; border-radius: 5px; }}
                    .team-section {{ background-color: #f9fafb; padding: 15px; margin: 15px 0; border-radius: 5px; }}
                    .metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 15px 0; }}
                    .metric-card {{ background-color: white; padding: 15px; border-radius: 5px; border: 1px solid #e5e7eb; text-align: center; }}
                    .metric-value {{ font-size: 24px; font-weight: bold; color: #16a34a; }}
                    .footer {{ background-color: #f9fafb; padding: 15px; text-align: center; font-size: 12px; color: #6b7280; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>📊 Weekly Team Report</h1>
                    <p>{company} - Week of {datetime.now().strftime('%B %d, %Y')}</p>
                </div>
                
                <div class="content">
                    <p>Hello {manager_name},</p>
                    
                    <div class="summary">
                        <h3>📈 Weekly Summary</h3>
                        <p>Here's how your team performed this week across key metrics.</p>
                    </div>
                    
                    <div class="metric-grid">
                        <div class="metric-card">
                            <div class="metric-value">{total_commits}</div>
                            <div>Total Commits</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{avg_complexity:.2f}</div>
                            <div>Avg Complexity</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{len(developers)}</div>
                            <div>Active Developers</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{total_meetings}</div>
                            <div>Total Meetings</div>
                        </div>
                    </div>
                    
                    <h3>👥 Team Breakdown</h3>
            """
            
            # Add team sections
            for team_name, team_devs in teams.items():
                team_commits = sum(d.get('commits', 0) for d in team_devs)
                team_avg_complexity = sum(d.get('entropy', 0) for d in team_devs) / len(team_devs) if team_devs else 0
                
                html_content += f"""
                    <div class="team-section">
                        <h4>{team_name} Team ({len(team_devs)} developers)</h4>
                        <p><strong>Commits:</strong> {team_commits} | <strong>Avg Complexity:</strong> {team_avg_complexity:.2f}</p>
                        <ul>
                """
                
                for dev in team_devs:
                    html_content += f"""
                            <li>{dev['name']} - {dev.get('commits', 0)} commits, {dev.get('meetings', 0)} meetings</li>
                    """
                
                html_content += """
                        </ul>
                    </div>
                """
            
            html_content += f"""
                    <h3>🎯 Key Insights</h3>
                    <ul>
                        <li>Team productivity is {"above" if total_commits > len(developers) * 10 else "at"} expected levels</li>
                        <li>Code complexity indicates {"high technical challenges" if avg_complexity > 0.7 else "standard development work"}</li>
                        <li>Meeting load is {"high" if total_meetings > len(developers) * 8 else "balanced"} across the team</li>
                    </ul>
                    
                    <p>
                        <a href="http://localhost:3000" style="background-color: #16a34a; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                            View Detailed Analytics
                        </a>
                    </p>
                </div>
                
                <div class="footer">
                    <p>DevLens Weekly Report • Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            </body>
            </html>
            """
        
        elif alert_type == "critical_issue":
            subject = f"🚨 Critical Performance Issue - {company}"
            
            # Find critical issues (simulated)
            critical_devs = [d for d in developers if d.get('commits', 0) == 0 or d.get('meetings', 0) > 20]
            
            html_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .header {{ background-color: #dc2626; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .critical {{ background-color: #fef2f2; border-left: 4px solid #dc2626; padding: 15px; margin: 15px 0; }}
                    .action-item {{ background-color: #fff7ed; border-left: 4px solid #f59e0b; padding: 10px; margin: 10px 0; }}
                    .footer {{ background-color: #f9fafb; padding: 15px; text-align: center; font-size: 12px; color: #6b7280; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🚨 Critical Alert</h1>
                    <p>Immediate attention required - {company}</p>
                </div>
                
                <div class="content">
                    <p>Hello {manager_name},</p>
                    
                    <div class="critical">
                        <strong>🚨 Critical Performance Issue Detected</strong><br>
                        We've identified performance patterns that require immediate attention.
                    </div>
                    
                    <h3>⚠️ Issues Identified</h3>
            """
            
            if critical_devs:
                html_content += "<ul>"
                for dev in critical_devs:
                    if dev.get('commits', 0) == 0:
                        html_content += f"<li><strong>{dev['name']}</strong> - No commits this week</li>"
                    elif dev.get('meetings', 0) > 20:
                        html_content += f"<li><strong>{dev['name']}</strong> - Excessive meeting load ({dev['meetings']} meetings)</li>"
                html_content += "</ul>"
            
            html_content += """
                    <h3>🎯 Immediate Actions Required</h3>
                    <div class="action-item">
                        <strong>1. Schedule immediate 1:1 meetings</strong> with affected team members
                    </div>
                    <div class="action-item">
                        <strong>2. Review workload distribution</strong> and remove blockers
                    </div>
                    <div class="action-item">
                        <strong>3. Assess meeting efficiency</strong> and reduce unnecessary meetings
                    </div>
                    
                    <p>
                        <a href="http://localhost:3000" style="background-color: #dc2626; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                            View Dashboard Now
                        </a>
                    </p>
                </div>
                
                <div class="footer">
                    <p>Critical Alert from DevLens Analytics • Immediate action recommended</p>
                </div>
            </body>
            </html>
            """
        
        return subject, html_content
    
    def send_performance_alert(self, to_email: str, manager_name: str, company: str, developers: List[Dict]):
        """Send performance alert email"""
        subject, html_content = self.generate_performance_alert_email(manager_name, company, developers, "performance_change")
        return self.send_email(to_email, subject, html_content)
    
    def send_weekly_report(self, to_email: str, manager_name: str, company: str, developers: List[Dict]):
        """Send weekly report email"""
        subject, html_content = self.generate_performance_alert_email(manager_name, company, developers, "weekly_report")
        return self.send_email(to_email, subject, html_content)
    
    def send_critical_issue_alert(self, to_email: str, manager_name: str, company: str, developers: List[Dict]):
        """Send critical issue alert email"""
        subject, html_content = self.generate_performance_alert_email(manager_name, company, developers, "critical_issue")
        return self.send_email(to_email, subject, html_content)
    
    def send_test_email(self, to_email: str, manager_name: str):
        """Send a test email to verify email configuration"""
        subject = "✅ DevLens Email Test - Configuration Successful"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #16a34a; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .success {{ background-color: #f0f9ff; border-left: 4px solid #16a34a; padding: 15px; margin: 15px 0; }}
                .footer {{ background-color: #f9fafb; padding: 15px; text-align: center; font-size: 12px; color: #6b7280; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>✅ Email Configuration Test</h1>
                <p>DevLens Analytics</p>
            </div>
            
            <div class="content">
                <p>Hello {manager_name},</p>
                
                <div class="success">
                    <strong>🎉 Success!</strong><br>
                    Your email notifications are now configured and working properly.
                </div>
                
                <h3>📧 What You'll Receive</h3>
                <ul>
                    <li><strong>Performance Alerts:</strong> When significant changes are detected in team performance</li>
                    <li><strong>Weekly Reports:</strong> Comprehensive team analytics every week</li>
                    <li><strong>Critical Issues:</strong> Immediate alerts for urgent performance issues</li>
                    <li><strong>Team Updates:</strong> Notifications about team member changes</li>
                </ul>
                
                <h3>⚙️ Manage Preferences</h3>
                <p>You can customize your notification preferences anytime in the DevLens dashboard settings.</p>
                
                <p>
                    <a href="http://localhost:3000" style="background-color: #16a34a; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                        Go to Dashboard
                    </a>
                </p>
            </div>
            
            <div class="footer">
                <p>DevLens Analytics • Test email sent on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content)