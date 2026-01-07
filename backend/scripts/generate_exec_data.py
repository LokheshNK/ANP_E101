import json
import random
from datetime import datetime, timedelta

NUM_USERS = 50
NUM_COMMITS = 1000  # High volume for better Y-axis distribution

start_time = datetime(2024, 5, 21, 8, 0, 0)

# Aligned with your comms data user IDs
users = [f"teams_guid_{i:03}" for i in range(1, NUM_USERS + 1)]

# Mock repository and file structure to calculate 'Centrality'
repos = ["core-auth", "payment-gateway", "frontend-main", "docs-site"]
file_types = [
    {"ext": ".ts", "impact": 1.0, "path": "src/logic/"},   # High Impact
    {"ext": ".py", "impact": 0.9, "path": "app/services/"},# High Impact
    {"ext": ".md", "impact": 0.1, "path": "docs/"},        # Low Impact
    {"ext": ".css", "impact": 0.3, "path": "styles/"}      # Med/Low Impact
]

commits = []

for i in range(1, NUM_COMMITS + 1):
    author_id = random.choice(users)
    repo = random.choice(repos)
    f_info = random.choice(file_types)
    
    # Randomize code changes
    additions = random.randint(1, 200)
    deletions = random.randint(0, 100)
    
    # This is the standard GitHub Commit object format
    commit = {
        "sha": f"sha_exec_{i:05}",
        "node_id": f"MDY6Q29tbWl0{i}",
        "commit": {
            "author": {
                "name": f"User {author_id[-3:]}",
                "email": f"user{author_id[-3:]}@company.com",
                "date": (start_time + timedelta(minutes=i * 5)).isoformat() + "Z"
            },
            "message": f"Update logic for {f_info['path']} in {repo}",
            "comment_count": random.randint(0, 5)
        },
        "url": f"https://api.github.com/repos/org/{repo}/commits/sha_{i}",
        # CUSTOM FIELDS for your DevLens Engine
        "devlens_meta": {
            "teams_user_id": author_id,  # THE JOIN KEY
            "file_impact_factor": f_info["impact"],
            "stats": {
                "additions": additions,
                "deletions": deletions,
                "total_entropy": (additions + deletions) * f_info["impact"]
            }
        }
    }
    
    commits.append(commit)

output_path = "C:/Users/ADMIN/Desktop/ANP_E101/backend/data/exec_mock_data.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(commits, f, indent=2)

print(f"Generated {NUM_COMMITS} GitHub commits for {NUM_USERS} users at {output_path}")