import json
import random
from datetime import datetime, timedelta

NUM_USERS = 25
NUM_MESSAGES = 800   # Increased for better distribution

start_time = datetime(2024, 5, 21, 8, 0, 0)

# Realistic team member names
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

# More varied technical messages with different complexity levels
high_tech_msgs = [
    "Implemented OAuth2 JWT refresh token rotation mechanism",
    "Optimized database connection pooling - reduced latency by 40%",
    "Refactored microservices architecture for better scalability",
    "Fixed critical memory leak in Redis caching layer",
    "Deployed blue-green deployment pipeline with zero downtime",
    "Integrated GraphQL federation across multiple services",
    "Implemented distributed tracing with Jaeger and OpenTelemetry"
]

medium_tech_msgs = [
    "Updated API endpoints for user authentication",
    "Fixed bug in payment processing workflow",
    "Added unit tests for core business logic",
    "Reviewed PR for database migration scripts",
    "Updated Docker containers for staging environment",
    "Implemented error handling for external API calls"
]

low_tech_msgs = [
    "Updated documentation for new features",
    "Fixed minor UI styling issues",
    "Added logging statements for debugging",
    "Updated package dependencies",
    "Fixed typos in error messages"
]

social_msgs = [
    "Good morning team! ☀️",
    "Anyone available for a quick sync?",
    "Great work on the release! 🎉",
    "Thanks for the code review!",
    "Let's discuss this in our standup",
    "Coffee break anyone? ☕",
    "Have a great weekend team!"
]

messages = []
message_ids = []

for i in range(1, NUM_MESSAGES + 1):
    msg_id = f"m_{i:04}"
    author = random.choice(team_members)

    # 25% chance this is a reply
    reply_to = random.choice(message_ids) if message_ids and random.random() < 0.25 else None

    # Different probability for different message types based on team
    if author["team"] in ["Backend", "DevOps"]:
        if random.random() < 0.5:
            content = random.choice(high_tech_msgs)
        elif random.random() < 0.3:
            content = random.choice(medium_tech_msgs)
        else:
            content = random.choice(social_msgs)
    elif author["team"] == "Frontend":
        if random.random() < 0.4:
            content = random.choice(medium_tech_msgs)
        elif random.random() < 0.3:
            content = random.choice(low_tech_msgs)
        else:
            content = random.choice(social_msgs)
    else:  # QA
        if random.random() < 0.3:
            content = random.choice(medium_tech_msgs)
        elif random.random() < 0.4:
            content = random.choice(low_tech_msgs)
        else:
            content = random.choice(social_msgs)

    msg = {
        "id": msg_id,
        "replyToId": reply_to,
        "createdDateTime": (start_time + timedelta(hours=i * 0.3)).isoformat() + "Z",
        "from": {
            "user": {
                "id": author["id"],
                "displayName": author["name"],
                "team": author["team"]
            }
        },
        "body": {
            "contentType": "html",
            "content": f"<div>{content}</div>"
        }
    }

    messages.append(msg)
    message_ids.append(msg_id)

with open("../data/comm_mock_data.json", "w", encoding="utf-8") as f:
    json.dump(messages, f, indent=2)

print(f"Generated {NUM_MESSAGES} messages for {NUM_USERS} team members across 4 teams")