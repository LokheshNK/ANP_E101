# DevLens Company-Based Data System

This system generates realistic company data with proper manager-developer hierarchies for the DevLens application.

## 🏢 What's Generated

### **4 Complete Companies** with different organizational cultures:

1. **TechCorp Solutions** (Enterprise Culture)
   - Manager: Sarah Chen (sarah.chen@techcorp.com / manager123)
   - Teams: Backend, Frontend, DevOps, QA
   - 15-20 developers with enterprise-focused work patterns

2. **Innovate Dynamics** (Startup Culture)
   - Manager: Alex Rodriguez (alex@innovate.io / startup456)
   - Teams: Full Stack, Mobile, Data Science
   - 10-15 developers with rapid development patterns

3. **AgileWorks Inc** (Agile Culture)
   - Manager: Jordan Kim (jordan.kim@agileworks.com / agile789)
   - Teams: Frontend, Backend, Platform, Security
   - 15-20 developers with collaboration-focused patterns

4. **CloudFirst Technologies** (Cloud-Native Culture)
   - Manager: Morgan Taylor (morgan@cloudfirst.tech / cloud2024)
   - Teams: Platform, Infrastructure, Security, API
   - 10-15 developers with infrastructure-focused patterns

## 🚀 Quick Start

### **One-Command Setup**
```bash
python backend/scripts/setup_devlens_data.py
```

This will:
1. Create companies, managers, teams, and developers in the database
2. Export data to JSON files for analytics compatibility
3. Calculate activity-based metrics

### **Individual Scripts**

1. **Generate Company Structure**
   ```bash
   python backend/scripts/generate_company_data.py
   ```

2. **Export to JSON Files**
   ```bash
   python backend/scripts/export_database_to_json.py "TechCorp Solutions"
   ```

3. **Calculate Activity Metrics**
   ```bash
   python backend/scripts/calculate_attendance_from_activity.py
   ```

## 🎯 Developer Archetypes

Each company generates developers with realistic performance profiles:

### **Enterprise (TechCorp Solutions)**
- **Senior Specialists**: High impact, low visibility (Hidden Gems)
- **Team Leads**: High impact, high visibility
- **Steady Contributors**: Balanced performance
- **Process Focused**: High meetings, lower technical output
- **Junior Developers**: Learning and growing

### **Startup (Innovate Dynamics)**
- **Full-Stack Heroes**: Very high impact, medium visibility
- **Growth Hackers**: High impact, high visibility
- **Rapid Prototypers**: High impact, low visibility (Hidden Gems)
- **Customer Focused**: Medium impact, high visibility
- **Fast Learners**: Growing quickly

### **Agile (AgileWorks Inc)**
- **Scrum Master Devs**: Medium impact, very high visibility
- **Technical Leads**: High impact, high visibility
- **Story Implementers**: Balanced contributors
- **Quality Advocates**: Focus on testing and quality
- **Continuous Learners**: Always improving

### **Cloud-Native (CloudFirst Technologies)**
- **Platform Engineers**: Very high impact, low visibility (Hidden Gems)
- **DevOps Specialists**: High impact, medium visibility
- **Reliability Engineers**: High impact, low visibility (Hidden Gems)
- **Automation Experts**: Medium impact, medium visibility
- **Cloud Architects**: High impact, high visibility

## 📊 Data Integration

### **Database Structure**
- Companies → Managers → Teams → Developers
- Proper foreign key relationships
- Authentication system for managers

### **JSON Export Compatibility**
- Communication data (Slack-like messages)
- Execution data (Git commits with entropy)
- HR behavioral data (attendance, collaboration)
- Activity-based metrics (calculated patterns)

### **Scoring Engine Integration**
- Works with existing `DevLensKeywordScorer`
- Quadrant analysis (Impact vs Visibility)
- Performance archetype classification
- Hidden Gems identification

## 🔧 Usage Examples

### **Login as Manager**
1. Start backend: `python backend/main.py`
2. Start frontend: `cd frontend && npm start`
3. Login with any manager credentials:
   - sarah.chen@techcorp.com / manager123
   - alex@innovate.io / startup456
   - jordan.kim@agileworks.com / agile789
   - morgan@cloudfirst.tech / cloud2024

### **View Different Company Cultures**
Each company shows different patterns:
- **TechCorp**: More process-oriented, steady development
- **Innovate**: Fast-paced, high-output developers
- **AgileWorks**: High collaboration, meeting-heavy culture
- **CloudFirst**: Technical specialists, infrastructure focus

### **Identify Hidden Gems**
Look for developers with:
- High technical impact (commits + entropy)
- Low visibility (few messages/meetings)
- Archetypes: Senior Specialists, Platform Engineers, Reliability Engineers

## 📈 Analytics Features

### **Performance Matrix**
- Impact vs Visibility quadrant analysis
- Star Performers, Hidden Gems, Team Connectors, Needs Support

### **Team Analytics**
- Attendance patterns from activity data
- Collaboration metrics from communication
- Technical contribution analysis
- Knowledge sharing indicators

### **Manager Dashboard**
- Company-wide performance overview
- Team-by-team breakdowns
- Individual developer insights
- Risk assessment and recommendations

## 🔄 Customization

### **Add New Companies**
Edit `company_templates` in `generate_company_data.py`:
```python
{
    "name": "Your Company",
    "culture": "your_culture",
    "manager": {
        "name": "Manager Name",
        "email": "manager@company.com",
        "password": "password123",
        "role": "Manager Title"
    },
    "teams": ["Team1", "Team2", "Team3"],
    "size": "medium"  # small, medium, large
}
```

### **Modify Developer Profiles**
Adjust archetype distributions in `generate_developer_profile()` method.

### **Change Company Size**
- `"small"`: 6-10 developers
- `"medium"`: 10-15 developers  
- `"large"`: 15-20 developers

## 🧪 Testing

### **Reset Database**
```bash
python backend/scripts/generate_company_data.py --reset
```

### **Export Specific Company**
```bash
python backend/scripts/export_database_to_json.py "Company Name"
```

### **Verify Setup**
```bash
python backend/test_data_generation.py
```

## 🎯 Key Benefits

1. **Realistic Hierarchies**: Proper company → manager → team → developer structure
2. **Cultural Diversity**: Different organizational patterns and work styles
3. **Hidden Gems Detection**: Identifies high-impact, low-visibility developers
4. **Manager Authentication**: Real login system with company-specific data
5. **Scalable Architecture**: Easy to add new companies and teams
6. **Analytics Ready**: Integrates with existing scoring and visualization systems

## 🔍 Troubleshooting

### **"Company already exists"**
- Use `--reset` flag to start fresh
- Or manually delete from database

### **No data in dashboard**
- Ensure you're logged in as the correct manager
- Check that JSON export completed successfully
- Verify backend is reading from correct data files

### **Unicode errors on Windows**
- All emoji characters have been removed for Windows compatibility

This system provides a complete, realistic foundation for testing and demonstrating DevLens with proper company hierarchies and diverse developer performance patterns.