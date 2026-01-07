import json
import random
from datetime import datetime, timedelta

NUM_USERS = 50
NUM_MESSAGES = 500   # change to 5_000 or 50_000 safely

start_time = datetime(2024, 5, 21, 8, 0, 0)

users = [
    {
        "id": f"teams_guid_{i:03}",
        "displayName": f"User {i}"
    }
    for i in range(1, NUM_USERS + 1)
]

technical_msgs = [
    "Auth token expiry needs review",
    "Database pool saturation observed",
    "Refactored caching logic",
    "PR ready for review",
    "CI pipeline failing intermittently",
    "JWT refresh flow updated",
    "Load testing results attached"
]

social_msgs = [
    "Good morning team ☀️",
    "Anyone free for a quick sync?",
    "Lunch break 🍽️",
    "Thanks for the update!",
    "Let’s discuss in standup"
]

messages = []
message_ids = []

for i in range(1, NUM_MESSAGES + 1):
    msg_id = f"m_{i:04}"
    author = random.choice(users)

    # 30% chance this is a reply
    reply_to = random.choice(message_ids) if message_ids and random.random() < 0.3 else None

    content = random.choice(
        technical_msgs if random.random() < 0.65 else social_msgs
    )

    msg = {
        "id": msg_id,
        "replyToId": reply_to,
        "createdDateTime": (start_time + timedelta(minutes=i * 2)).isoformat() + "Z",
        "from": {
            "user": {
                "id": author["id"],
                "displayName": author["displayName"]
            }
        },
        "body": {
            "contentType": "html",
            "content": f"<div>{content}</div>"
        }
    }

    messages.append(msg)
    message_ids.append(msg_id)

with open("C:/Users/ADMIN/Desktop/ANP_E101/backend/data/comm_mock_data.json", "w", encoding="utf-8") as f:
    json.dump(messages, f, indent=2)

print(f"Generated {NUM_MESSAGES} messages for {NUM_USERS} users")
