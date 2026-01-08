from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Union
import hashlib
import json
from database import DevLensDB
from email_service import EmailService
from engine.nlp_filter import analyze_communication
from engine.scoring import process_metrics
from engine.nlp_visibility_scorer import analyze_message_visibility

app = FastAPI(title="DevLens API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database and email service
db = DevLensDB()
email_service = EmailService()

# Pydantic models for request/response
class LoginRequest(BaseModel):
    email: str
    password: str
    company: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    company_name: str

class EmailSettingsRequest(BaseModel):
    manager_id: int
    email_address: str
    email_alerts: bool = True
    performance_alerts: bool = True
    weekly_reports: bool = False
    team_updates: bool = True
    critical_issues: bool = True

class SendEmailRequest(BaseModel):
    email_type: str  # 'test', 'performance', 'weekly', 'critical'
    manager_id: int

class AnalyzeVisibilityRequest(BaseModel):
    messages: Union[List[str], List[dict], str]
    developer_name: Optional[str] = None
    meeting_hours: Optional[float] = 0.0

@app.get("/")
def read_root():
    return {"status": "DevLens API is Running"}

@app.get("/api/companies")
def get_companies():
    """Get all companies"""
    companies = db.get_companies()
    return {
        "success": True,
        "companies": [{"id": comp[0], "name": comp[1]} for comp in companies]
    }

@app.post("/api/login")
def login(request: LoginRequest):
    """Authenticate manager login"""
    # Hash the password
    password_hash = hashlib.sha256(request.password.encode()).hexdigest()
    
    # Check credentials with company validation
    manager = db.authenticate_manager(request.email, password_hash, request.company)
    
    if manager:
        return {
            "success": True,
            "user": {
                "id": manager["id"],
                "email": manager["email"],
                "name": manager["name"],
                "role": manager["role"],
                "company": manager["company"]  # Use the company from the database response
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/register")
def register(request: RegisterRequest):
    """Register new manager and company"""
    # Hash the password
    password_hash = hashlib.sha256(request.password.encode()).hexdigest()
    
    try:
        # Create company and manager
        manager_id = db.create_company_and_manager(
            company_name=request.company_name,
            manager_email=request.email,
            manager_password=password_hash,
            manager_name=request.name
        )
        
        if manager_id:
            return {
                "success": True,
                "message": "Registration successful",
                "manager_id": manager_id
            }
        else:
            raise HTTPException(status_code=400, detail="Registration failed")
            
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=400, detail="Email already exists")
        else:
            raise HTTPException(status_code=400, detail="Registration failed")

@app.post("/api/managers")
def create_manager(request: RegisterRequest):
    """Create new manager and company (alternative endpoint for registration)"""
    return register(request)

@app.get("/api/dashboard/{company_name}")
def get_dashboard_data(company_name: str):
    """Get dashboard data for a specific company (main endpoint used by frontend)"""
    # Decode URL-encoded company name
    from urllib.parse import unquote
    company_name = unquote(company_name)
    
    # Get developers for this company
    developers = db.get_company_developers(company_name)
    
    if not developers:
        raise HTTPException(status_code=404, detail=f"No developers found for company: {company_name}")
    
    # Process communication scores
    for dev in developers:
        dev["comm_score"] = analyze_communication(dev["msgs"])
    
    # Process metrics using the scoring engine
    processed_data = process_metrics(developers)
    
    # Load attendance data if available
    attendance_data = {}
    try:
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        attendance_file = os.path.join(script_dir, "data", "activity_based_metrics.json")
        
        if os.path.exists(attendance_file):
            with open(attendance_file, 'r', encoding='utf-8') as f:
                attendance_list = json.load(f)
                # Convert to dict for easy lookup
                for att in attendance_list:
                    attendance_data[att['name']] = att
    except Exception as e:
        print(f"Could not load attendance data: {e}")
    
    # Add attendance data to processed developers
    for dev in processed_data:
        if dev['name'] in attendance_data:
            att_info = attendance_data[dev['name']]
            dev['attendance_rate'] = att_info['attendance_metrics']['attendance_rate']
            dev['days_present'] = att_info['attendance_metrics']['days_present']
            dev['total_work_days'] = att_info['attendance_metrics']['total_work_days']
            dev['behavioral_summary'] = att_info.get('behavioral_summary', {})
        else:
            # Default attendance if not found
            dev['attendance_rate'] = 0.85  # Default 85%
            dev['days_present'] = 17
            dev['total_work_days'] = 20
            dev['behavioral_summary'] = {}
    
    return {
        "company": company_name,
        "developers": processed_data,
        "total_count": len(processed_data)
    }

@app.get("/api/dashboard/manager/{manager_id}")
def get_dashboard_data_by_manager(manager_id: int):
    """Get dashboard data for a specific manager"""
    # Get manager's company
    manager = db.get_manager_by_id(manager_id)
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    
    company_id = manager[5]  # company_id is at index 5
    
    # Get company name
    company = db.get_company_by_id(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    company_name = company[1]  # name is at index 1
    
    # Get developers for this company
    developers = db.get_company_developers(company_name)
    
    # Process communication scores
    for dev in developers:
        dev["comm_score"] = analyze_communication(dev["msgs"])
    
    # Process metrics using the scoring engine
    processed_data = process_metrics(developers)
    
    # Load attendance data if available
    attendance_data = {}
    try:
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        attendance_file = os.path.join(script_dir, "data", "activity_based_metrics.json")
        
        if os.path.exists(attendance_file):
            with open(attendance_file, 'r', encoding='utf-8') as f:
                attendance_list = json.load(f)
                # Convert to dict for easy lookup
                for att in attendance_list:
                    attendance_data[att['name']] = att
    except Exception as e:
        print(f"Could not load attendance data: {e}")
    
    # Add attendance data to processed developers
    for dev in processed_data:
        if dev['name'] in attendance_data:
            att_info = attendance_data[dev['name']]
            dev['attendance_rate'] = att_info['attendance_metrics']['attendance_rate']
            dev['days_present'] = att_info['attendance_metrics']['days_present']
            dev['total_work_days'] = att_info['attendance_metrics']['total_work_days']
            dev['behavioral_summary'] = att_info.get('behavioral_summary', {})
        else:
            # Default attendance if not found
            dev['attendance_rate'] = 0.85  # Default 85%
            dev['days_present'] = 17
            dev['total_work_days'] = 20
            dev['behavioral_summary'] = {}
    
    return {
        "company": company_name,
        "developers": processed_data,
        "total_count": len(processed_data)
    }

@app.get("/api/team-analytics/{company_name}")
def get_team_analytics_by_company(company_name: str):
    """Get team analytics for a specific company"""
    # Decode URL-encoded company name
    from urllib.parse import unquote
    company_name = unquote(company_name)
    
    # Get developers for this company
    developers = db.get_company_developers(company_name)
    
    if not developers:
        raise HTTPException(status_code=404, detail=f"No developers found for company: {company_name}")
    
    # Process communication scores
    for dev in developers:
        dev["comm_score"] = analyze_communication(dev["msgs"])
    
    # Process metrics
    processed_data = process_metrics(developers)
    
    # Group by teams
    teams = {}
    for dev in processed_data:
        team_name = dev["team"]
        if team_name not in teams:
            teams[team_name] = {
                "name": team_name,
                "members": [],
                "stats": {
                    "total_commits": 0,
                    "avg_entropy": 0,
                    "total_meetings": 0,
                    "avg_comm_score": 0
                }
            }
        teams[team_name]["members"].append(dev)
    
    # Calculate team statistics
    for team_name, team_data in teams.items():
        members = team_data["members"]
        if members:
            team_data["stats"]["total_commits"] = sum(m["commits"] for m in members)
            team_data["stats"]["avg_entropy"] = sum(m["entropy"] for m in members) / len(members)
            team_data["stats"]["total_meetings"] = sum(m["meetings"] for m in members)
            team_data["stats"]["avg_comm_score"] = sum(m["comm_score"] for m in members) / len(members)
            team_data["stats"]["member_count"] = len(members)
    
    return {
        "company": company_name,
        "teams": list(teams.values()),
        "total_developers": len(processed_data)
    }

@app.get("/api/hidden-gems/{company_name}")
def get_hidden_gems_by_company(company_name: str):
    """Get Hidden Gems (Quadrant 2 - High Impact, Low Visibility) for a specific company"""
    # Decode URL-encoded company name
    from urllib.parse import unquote
    company_name = unquote(company_name)
    
    # Get developers for this company
    developers = db.get_company_developers(company_name)
    
    if not developers:
        raise HTTPException(status_code=404, detail=f"No developers found for company: {company_name}")
    
    # Process communication scores
    for dev in developers:
        dev["comm_score"] = analyze_communication(dev["msgs"])
    
    # Process metrics
    processed_data = process_metrics(developers)
    
    # Filter only Hidden Gems (Quadrant 2)
    hidden_gems = [dev for dev in processed_data if dev.get('is_hidden_gem', False)]
    
    # Sort Hidden Gems by impact score (descending)
    hidden_gems.sort(key=lambda x: x.get('raw_impact', 0), reverse=True)
    
    return {
        "company": company_name,
        "hidden_gems": hidden_gems,
        "total_hidden_gems": len(hidden_gems),
        "total_developers": len(processed_data)
    }

@app.get("/api/settings/{manager_id}")
def get_manager_settings(manager_id: int):
    """Get manager's email settings"""
    settings = db.get_manager_settings(manager_id)
    
    if settings:
        return {
            "success": True,
            "settings": settings
        }
    else:
        raise HTTPException(status_code=404, detail="Settings not found")

@app.post("/api/settings")
def update_manager_settings(request: EmailSettingsRequest):
    """Update manager's email settings"""
    success = db.update_manager_settings(
        request.manager_id,
        request.email_address,
        request.email_alerts,
        request.performance_alerts,
        request.weekly_reports,
        request.team_updates,
        request.critical_issues
    )
    
    if success:
        return {"success": True, "message": "Settings updated successfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to update settings")

@app.post("/api/send-email")
def send_email(request: SendEmailRequest):
    """Send email notification"""
    # Get manager info and settings
    settings = db.get_manager_settings(request.manager_id)
    if not settings:
        raise HTTPException(status_code=404, detail="Email settings not found")
    
    # Use the custom email address from settings
    email_address = settings['email_address']
    
    # Get manager info for name and company
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT m.name, c.name as company_name
        FROM managers m
        JOIN companies c ON m.company_id = c.id
        WHERE m.id = ?
    ''', (request.manager_id,))
    
    manager_result = cursor.fetchone()
    conn.close()
    
    if not manager_result:
        raise HTTPException(status_code=404, detail="Manager not found")
    
    manager_name, company_name = manager_result
    
    # Get company developers for email content
    developers = db.get_company_developers(company_name)
    
    # Process developers for email content
    for dev in developers:
        dev["comm_score"] = analyze_communication(dev["msgs"])
    processed_data = process_metrics(developers)
    
    # Send appropriate email based on type
    success = False
    
    if request.email_type == "test":
        success = email_service.send_test_email(email_address, manager_name)
    elif request.email_type == "performance" and settings['performance_alerts']:
        success = email_service.send_performance_alert(email_address, manager_name, company_name, processed_data)
    elif request.email_type == "weekly" and settings['weekly_reports']:
        success = email_service.send_weekly_report(email_address, manager_name, company_name, processed_data)
    elif request.email_type == "critical" and settings['critical_issues']:
        success = email_service.send_critical_issue_alert(email_address, manager_name, company_name, processed_data)
    else:
        raise HTTPException(status_code=400, detail="Invalid email type or notifications disabled")
    
    if success:
        return {"success": True, "message": f"Email sent successfully to {email_address}"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email")

@app.post("/api/analyze-visibility")
def analyze_visibility(request: AnalyzeVisibilityRequest):
    """
    Analyze message visibility using advanced NLP techniques
    
    This endpoint uses AI/NLP to analyze message content and calculate visibility scores
    based on technical impact, leadership, knowledge sharing, and collaboration patterns.
    """
    try:
        # Use the NLP visibility scorer to analyze messages (including meeting hours)
        analysis_result = analyze_message_visibility(request.messages, request.meeting_hours)
        
        # Add developer name if provided
        if request.developer_name:
            analysis_result['developer_name'] = request.developer_name
        
        return {
            "success": True,
            "analysis": analysis_result,
            "message": "NLP visibility analysis completed successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/nlp-visibility-demo/{company_name}")
def get_nlp_visibility_demo(company_name: str):
    """
    Demo endpoint showing NLP visibility analysis for all developers in a company
    """
    # Decode URL-encoded company name
    from urllib.parse import unquote
    company_name = unquote(company_name)
    
    # Get developers for this company
    developers = db.get_company_developers(company_name)
    
    if not developers:
        raise HTTPException(status_code=404, detail=f"No developers found for company: {company_name}")
    
    nlp_results = []
    
    for dev in developers:
        messages = dev.get('msgs', [])
        
        # Analyze using NLP visibility scorer (including meeting hours)
        meeting_hours = dev.get('meetings', 0) * 1.5  # Assume 1.5 hours per meeting
        nlp_analysis = analyze_message_visibility(messages, meeting_hours)
        
        # Also get legacy analysis for comparison
        legacy_comm_score = analyze_communication(messages)
        
        nlp_results.append({
            'developer_name': dev['name'],
            'team': dev['team'],
            'message_count': len(messages),
            'nlp_visibility_analysis': nlp_analysis,
            'legacy_comm_score': legacy_comm_score,
            'commits': dev.get('commits', 0),
            'entropy': dev.get('entropy', 0.0),
            'meetings': dev.get('meetings', 0)
        })
    
    # Sort by NLP visibility score (descending)
    nlp_results.sort(key=lambda x: x['nlp_visibility_analysis']['visibility_score'], reverse=True)
    
    return {
        "company": company_name,
        "nlp_visibility_analysis": nlp_results,
        "total_developers": len(nlp_results),
        "analysis_info": {
            "description": "Advanced NLP-based visibility scoring using AI techniques",
            "components": [
                "Technical Impact (25%): Technical contributions and expertise",
                "Leadership Influence (20%): Decision making and strategic thinking", 
                "Knowledge Sharing (20%): Teaching, documentation, and mentoring",
                "Problem Solving (15%): Helping others and troubleshooting",
                "Collaboration (10%): Team engagement and communication",
                "Meeting Engagement (8%): Meeting hours (requires communication)",
                "Urgency Priority (1%): Handling critical and urgent matters",
                "Engagement Questions (1%): Active participation and curiosity"
            ]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)