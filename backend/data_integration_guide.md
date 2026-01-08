# DevLens Data Integration Guide
## How to Obtain Real-World Behavioral Metrics

### 🏢 **ATTENDANCE & RELIABILITY DATA**

#### **Data Sources:**
- **HR Management Systems**: Workday, BambooHR, ADP
- **Time Tracking Tools**: Toggl, Harvest, Clockify
- **Calendar Systems**: Google Calendar, Outlook, Calendly

#### **API Integration Examples:**
```python
# Example: BambooHR API for attendance
import requests

def get_attendance_data(employee_id, start_date, end_date):
    headers = {'Authorization': f'Basic {bamboo_api_key}'}
    url = f'https://api.bamboohr.com/api/gateway.php/{company_domain}/v1/employees/{employee_id}/time_off'
    
    response = requests.get(url, headers=headers, params={
        'start': start_date,
        'end': end_date
    })
    
    return response.json()

# Example: Google Calendar API for meeting attendance
from googleapiclient.discovery import build

def get_meeting_attendance(employee_email, start_date, end_date):
    service = build('calendar', 'v3', credentials=creds)
    
    events = service.events().list(
        calendarId=employee_email,
        timeMin=start_date,
        timeMax=end_date,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    return events.get('items', [])
```

#### **Calculated Metrics:**
- **Leave Days**: Sum of approved vacation/personal days
- **Sick Days**: Sum of sick leave taken
- **Meeting Attendance Rate**: (Meetings attended / Total meetings invited) × 100
- **Attendance Rate**: (Work days present / Total work days) × 100

---

### 🤝 **COLLABORATION & TEAMWORK DATA**

#### **Data Sources:**
- **Git Platforms**: GitHub, GitLab, Bitbucket APIs
- **Code Review Tools**: GitHub PR API, GitLab MR API, Gerrit
- **Project Management**: Jira, Azure DevOps, Linear
- **Communication**: Slack, Microsoft Teams, Discord

#### **API Integration Examples:**
```python
# Example: GitHub API for code reviews
def get_code_review_metrics(username, org, start_date, end_date):
    headers = {'Authorization': f'token {github_token}'}
    
    # Reviews given
    reviews_given = requests.get(
        f'https://api.github.com/search/issues',
        headers=headers,
        params={
            'q': f'type:pr reviewed-by:{username} org:{org} created:{start_date}..{end_date}',
            'per_page': 100
        }
    ).json()
    
    # Reviews received
    reviews_received = requests.get(
        f'https://api.github.com/search/issues',
        headers=headers,
        params={
            'q': f'type:pr author:{username} org:{org} created:{start_date}..{end_date}',
            'per_page': 100
        }
    ).json()
    
    return {
        'reviews_given': reviews_given['total_count'],
        'reviews_received': reviews_received['total_count']
    }

# Example: Slack API for cross-team interactions
def get_slack_interactions(user_id, start_date, end_date):
    headers = {'Authorization': f'Bearer {slack_token}'}
    
    # Get user's messages across channels
    conversations = requests.get(
        'https://slack.com/api/conversations.list',
        headers=headers,
        params={'types': 'public_channel,private_channel'}
    ).json()
    
    cross_team_count = 0
    for channel in conversations['channels']:
        # Analyze channel membership and user participation
        # Count interactions with users from different teams
        pass
    
    return cross_team_count
```

#### **Calculated Metrics:**
- **Code Reviews Given**: Count of PR/MR reviews submitted
- **Review Response Time**: Average time to respond to review requests
- **Cross-team Interactions**: Messages/comments with users from other teams
- **Pair Programming Hours**: Calendar events tagged as "pair programming"

---

### 📚 **KNOWLEDGE SHARING DATA**

#### **Data Sources:**
- **Documentation Platforms**: Confluence, Notion, GitBook, Wiki systems
- **Learning Management**: Coursera for Business, Udemy Business, internal LMS
- **Video Platforms**: Loom, internal training videos
- **Q&A Platforms**: Stack Overflow for Teams, internal forums

#### **API Integration Examples:**
```python
# Example: Confluence API for documentation contributions
def get_confluence_contributions(user_id, space_key, start_date, end_date):
    auth = (confluence_username, confluence_api_token)
    base_url = 'https://your-domain.atlassian.net/wiki/rest/api'
    
    # Get pages created/updated by user
    response = requests.get(
        f'{base_url}/content',
        auth=auth,
        params={
            'spaceKey': space_key,
            'expand': 'history.lastUpdated',
            'limit': 1000
        }
    )
    
    pages = response.json()['results']
    user_contributions = []
    
    for page in pages:
        if page['history']['lastUpdated']['by']['userKey'] == user_id:
            user_contributions.append(page)
    
    return len(user_contributions)

# Example: Internal mentoring system API
def get_mentoring_sessions(mentor_id, start_date, end_date):
    # This would connect to your internal mentoring platform
    response = requests.get(
        f'{internal_api_base}/mentoring/sessions',
        headers={'Authorization': f'Bearer {internal_token}'},
        params={
            'mentor_id': mentor_id,
            'start_date': start_date,
            'end_date': end_date
        }
    )
    
    return response.json()['session_count']
```

#### **Calculated Metrics:**
- **Wiki Contributions**: Pages created/edited in documentation systems
- **Mentoring Sessions**: Formal mentoring meetings conducted
- **Help Requests Answered**: Responses in internal Q&A systems
- **Conference Talks**: Speaking engagements (internal/external)

---

### 💡 **INNOVATION & INITIATIVE DATA**

#### **Data Sources:**
- **Issue Tracking**: Jira, GitHub Issues, Linear, Azure DevOps
- **Innovation Platforms**: Internal suggestion systems, hackathon platforms
- **Process Management**: Process documentation systems, improvement tracking

#### **API Integration Examples:**
```python
# Example: Jira API for feature proposals and bug reports
def get_jira_initiatives(user_email, project_key, start_date, end_date):
    auth = (jira_username, jira_api_token)
    base_url = 'https://your-domain.atlassian.net/rest/api/3'
    
    # Feature proposals (issues created with specific labels)
    jql_features = f'project = {project_key} AND reporter = "{user_email}" AND labels = "feature-proposal" AND created >= "{start_date}" AND created <= "{end_date}"'
    
    features = requests.get(
        f'{base_url}/search',
        auth=auth,
        params={'jql': jql_features}
    ).json()
    
    # Bug reports filed
    jql_bugs = f'project = {project_key} AND reporter = "{user_email}" AND issuetype = "Bug" AND created >= "{start_date}" AND created <= "{end_date}"'
    
    bugs = requests.get(
        f'{base_url}/search',
        auth=auth,
        params={'jql': jql_bugs}
    ).json()
    
    return {
        'feature_proposals': features['total'],
        'bug_reports': bugs['total']
    }

# Example: Internal innovation platform
def get_process_improvements(employee_id, start_date, end_date):
    # Connect to internal process improvement tracking system
    response = requests.get(
        f'{internal_api_base}/improvements',
        headers={'Authorization': f'Bearer {internal_token}'},
        params={
            'submitter_id': employee_id,
            'start_date': start_date,
            'end_date': end_date,
            'status': 'implemented'
        }
    )
    
    return response.json()['improvement_count']
```

#### **Calculated Metrics:**
- **Feature Proposals**: Issues/tickets created with "enhancement" labels
- **Process Improvements**: Documented process changes implemented
- **Bug Reports Filed**: Proactive bug identification and reporting
- **Innovation Score**: Weighted combination of creative contributions

---

### 📈 **LEARNING & DEVELOPMENT DATA**

#### **Data Sources:**
- **Learning Management Systems**: Coursera, Udemy, internal LMS
- **Certification Platforms**: Credly, Accredible, vendor certification systems
- **Conference Platforms**: Event management systems, speaking bureau data

#### **API Integration Examples:**
```python
# Example: Coursera for Business API
def get_coursera_progress(learner_id, start_date, end_date):
    headers = {'Authorization': f'Bearer {coursera_api_token}'}
    
    response = requests.get(
        f'https://api.coursera.org/api/externalBasicProfiles.v1/{learner_id}/courseProgress',
        headers=headers,
        params={
            'start': start_date,
            'end': end_date
        }
    )
    
    courses = response.json()['elements']
    total_hours = sum(course.get('timeSpentHours', 0) for course in courses)
    
    return total_hours

# Example: Credly API for certifications
def get_certifications(badge_earner_email, start_date, end_date):
    headers = {'Authorization': f'Basic {credly_api_key}'}
    
    response = requests.get(
        'https://api.credly.com/v1/badges',
        headers=headers,
        params={
            'filter[badge_earner_email]': badge_earner_email,
            'filter[issued_after]': start_date,
            'filter[issued_before]': end_date
        }
    )
    
    return len(response.json()['data'])
```

#### **Calculated Metrics:**
- **Training Hours**: Time spent in formal learning activities
- **Certifications Earned**: Professional certifications obtained
- **Course Completions**: Online courses completed
- **Learning Velocity**: Rate of skill acquisition over time

---

## 🔧 **Implementation Architecture**

### **Data Pipeline Structure:**
```python
class DevLensDataPipeline:
    def __init__(self):
        self.integrations = {
            'hr_system': BambooHRIntegration(),
            'git_platform': GitHubIntegration(),
            'communication': SlackIntegration(),
            'documentation': ConfluenceIntegration(),
            'learning': CourseraIntegration(),
            'project_management': JiraIntegration()
        }
    
    def collect_all_metrics(self, employee_id, start_date, end_date):
        metrics = {}
        
        # Collect from each integration
        for system_name, integration in self.integrations.items():
            try:
                metrics[system_name] = integration.get_metrics(
                    employee_id, start_date, end_date
                )
            except Exception as e:
                print(f"Failed to collect from {system_name}: {e}")
                metrics[system_name] = {}
        
        return self.normalize_metrics(metrics)
    
    def normalize_metrics(self, raw_metrics):
        # Convert raw data into standardized DevLens format
        return {
            'attendance_metrics': self._normalize_attendance(raw_metrics['hr_system']),
            'collaboration_metrics': self._normalize_collaboration(raw_metrics['git_platform']),
            'knowledge_sharing_metrics': self._normalize_knowledge(raw_metrics['documentation']),
            'innovation_metrics': self._normalize_innovation(raw_metrics['project_management']),
            'learning_metrics': self._normalize_learning(raw_metrics['learning'])
        }
```

### **Key Implementation Considerations:**

1. **🔐 Privacy & Security**: Ensure GDPR/privacy compliance
2. **🔄 Real-time vs Batch**: Balance between real-time updates and system performance
3. **📊 Data Quality**: Handle missing data and outliers gracefully
4. **🎯 Normalization**: Standardize metrics across different team sizes and roles
5. **⚡ Performance**: Cache frequently accessed data and use efficient APIs

This comprehensive approach transforms DevLens from a simple Git+Slack analyzer into a **holistic developer performance platform** that captures the full spectrum of professional contribution and growth.