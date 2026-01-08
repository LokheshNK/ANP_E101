-import json
import random
from datetime import datetime, timedelta

NUM_USERS = 25
ANALYSIS_PERIOD_DAYS = 90  # 3 months

start_date = datetime(2024, 5, 21)
end_date = start_date + timedelta(days=ANALYSIS_PERIOD_DAYS)

# Team member data aligned with other datasets
team_members = [
    {"id": f"teams_guid_{i:03}", "name": name, "team": team}
    for i, (name, team) in enumerate([
        ("Alex Chen", "Frontend"), ("Sarah Johnson", "Backend"), ("Mike Rodriguez", "DevOps"),
        ("Emily Davis", "Frontend"), ("James Wilson", "Backend"), ("Lisa Zhang", "QA"),
        ("David Kim", "Frontend"), ("Rachel Green", "Backend"), ("Tom Anderson", "DevOps"),
        ("Maria Garcia", "QA"), ("Kevin Lee", "Frontend"), ("Anna Smith", "Backend"),
        ("Chris Brown", "DevOps"), ("Jessica Taylor", "QA"), ("Ryan Murphy", "Frontend"),
        ("Sophie Wang", "Backend"), ("Daniel Clark", "DevOps"), ("Amy Liu", "QA"),
        ("Mark Thompson", "Frontend"), ("Grace Park", "Backend"), ("Jason Miller", "DevOps"),
        ("Olivia Chen", "QA"), ("Nathan Davis", "Frontend"), ("Emma Wilson", "Backend"),
        ("Lucas Garcia", "DevOps")
    ], 1)
]

def generate_hr_metrics():
    """Generate comprehensive HR and behavioral metrics"""
    hr_data = []
    
    for member in team_members:
        # Base personality traits that influence other metrics
        personality_traits = {
            "collaboration_tendency": random.uniform(0.3, 1.0),
            "knowledge_sharing_tendency": random.uniform(0.2, 1.0),
            "meeting_engagement": random.uniform(0.4, 1.0),
            "proactivity_level": random.uniform(0.3, 1.0),
            "reliability_factor": random.uniform(0.6, 1.0)
        }
        
        # Attendance & Leave Management
        total_work_days = ANALYSIS_PERIOD_DAYS - 26  # Exclude weekends (rough estimate)
        leave_days = int(random.uniform(2, 15) * (1 - personality_traits["reliability_factor"]))
        sick_days = int(random.uniform(0, 8) * (1 - personality_traits["reliability_factor"]))
        attendance_rate = (total_work_days - leave_days - sick_days) / total_work_days
        
        # Meeting & Collaboration Metrics
        total_meetings = random.randint(40, 120)
        meetings_attended = int(total_meetings * attendance_rate * personality_traits["meeting_engagement"])
        meetings_organized = int(random.uniform(2, 15) * personality_traits["proactivity_level"])
        
        # Knowledge Sharing & Documentation
        wiki_contributions = int(random.uniform(5, 50) * personality_traits["knowledge_sharing_tendency"])
        documentation_updates = int(random.uniform(3, 25) * personality_traits["knowledge_sharing_tendency"])
        knowledge_base_articles = int(random.uniform(1, 12) * personality_traits["knowledge_sharing_tendency"])
        
        # Code Review & Collaboration
        code_reviews_given = int(random.uniform(10, 80) * personality_traits["collaboration_tendency"])
        code_reviews_received = int(random.uniform(8, 40))
        review_response_time_hours = random.uniform(2, 48) * (2 - personality_traits["collaboration_tendency"])
        
        # Mentoring & Support
        mentoring_sessions = int(random.uniform(0, 20) * personality_traits["knowledge_sharing_tendency"])
        help_requests_answered = int(random.uniform(5, 60) * personality_traits["collaboration_tendency"])
        pair_programming_hours = int(random.uniform(2, 40) * personality_traits["collaboration_tendency"])
        
        # Innovation & Initiative
        feature_proposals = int(random.uniform(1, 10) * personality_traits["proactivity_level"])
        bug_reports_filed = int(random.uniform(3, 25) * personality_traits["proactivity_level"])
        process_improvements = int(random.uniform(0, 8) * personality_traits["proactivity_level"])
        
        # Learning & Development
        training_hours = random.uniform(10, 80) * personality_traits["proactivity_level"]
        certifications_earned = random.randint(0, 3) if personality_traits["proactivity_level"] > 0.7 else 0
        conference_talks = random.randint(0, 2) if personality_traits["knowledge_sharing_tendency"] > 0.8 else 0
        
        # Communication Quality (derived from Slack analysis)
        avg_response_time_minutes = random.uniform(15, 240) * (2 - personality_traits["collaboration_tendency"])
        cross_team_interactions = int(random.uniform(10, 100) * personality_traits["collaboration_tendency"])
        
        # Team-specific adjustments
        team_multipliers = {
            "Backend": {"code_reviews_given": 1.3, "documentation_updates": 1.2},
            "Frontend": {"cross_team_interactions": 1.2, "feature_proposals": 1.1},
            "DevOps": {"process_improvements": 1.5, "help_requests_answered": 1.3},
            "QA": {"bug_reports_filed": 2.0, "documentation_updates": 1.4}
        }
        
        if member["team"] in team_multipliers:
            multipliers = team_multipliers[member["team"]]
            for metric, multiplier in multipliers.items():
                if metric in locals():
                    locals()[metric] = int(locals()[metric] * multiplier)
        
        hr_record = {
            "user_id": member["id"],
            "name": member["name"],
            "team": member["team"],
            "analysis_period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_days": ANALYSIS_PERIOD_DAYS
            },
            "attendance_metrics": {
                "total_work_days": total_work_days,
                "days_present": total_work_days - leave_days - sick_days,
                "leave_days": leave_days,
                "sick_days": sick_days,
                "attendance_rate": round(attendance_rate, 3)
            },
            "collaboration_metrics": {
                "meetings_attended": meetings_attended,
                "meetings_organized": meetings_organized,
                "meeting_attendance_rate": round(meetings_attended / total_meetings, 3),
                "code_reviews_given": code_reviews_given,
                "code_reviews_received": code_reviews_received,
                "avg_review_response_time_hours": round(review_response_time_hours, 1),
                "cross_team_interactions": cross_team_interactions,
                "pair_programming_hours": pair_programming_hours
            },
            "knowledge_sharing_metrics": {
                "wiki_contributions": wiki_contributions,
                "documentation_updates": documentation_updates,
                "knowledge_base_articles": knowledge_base_articles,
                "mentoring_sessions": mentoring_sessions,
                "help_requests_answered": help_requests_answered,
                "conference_talks": conference_talks
            },
            "innovation_metrics": {
                "feature_proposals": feature_proposals,
                "bug_reports_filed": bug_reports_filed,
                "process_improvements": process_improvements
            },
            "learning_metrics": {
                "training_hours": round(training_hours, 1),
                "certifications_earned": certifications_earned
            },
            "communication_metrics": {
                "avg_response_time_minutes": round(avg_response_time_minutes, 1)
            },
            "personality_indicators": {
                "collaboration_score": round(personality_traits["collaboration_tendency"], 3),
                "knowledge_sharing_score": round(personality_traits["knowledge_sharing_tendency"], 3),
                "proactivity_score": round(personality_traits["proactivity_level"], 3),
                "reliability_score": round(personality_traits["reliability_factor"], 3)
            }
        }
        
        hr_data.append(hr_record)
    
    return hr_data

# Generate the data
hr_metrics = generate_hr_metrics()

# Save to file
output_path = "../data/hr_behavioral_data.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(hr_metrics, f, indent=2)

print(f"Generated comprehensive HR and behavioral data for {NUM_USERS} team members")
print(f"Metrics include: attendance, collaboration, knowledge sharing, innovation, learning")
print(f"Sample metrics for {hr_metrics[0]['name']}:")
print(f"  - Attendance Rate: {hr_metrics[0]['attendance_metrics']['attendance_rate']}")
print(f"  - Code Reviews Given: {hr_metrics[0]['collaboration_metrics']['code_reviews_given']}")
print(f"  - Knowledge Sharing Score: {hr_metrics[0]['personality_indicators']['knowledge_sharing_score']}")