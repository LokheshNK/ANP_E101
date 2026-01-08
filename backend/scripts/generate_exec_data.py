import json
import random
import math
from datetime import datetime, timedelta

NUM_USERS = 25
NUM_COMMITS = 1200  # Increased for better distribution

start_time = datetime(2024, 5, 21, 8, 0, 0)

# Aligned with communication data user IDs and names
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

# Mock repository and file structure to calculate 'Centrality'
repos = ["core-auth", "payment-gateway", "frontend-main", "docs-site", "api-gateway", "user-service"]

# Different file types with varying impact based on team specialization
file_types = {
    "Backend": [
        {"ext": ".py", "impact": 1.2, "path": "src/services/"},
        {"ext": ".js", "impact": 1.0, "path": "src/api/"},
        {"ext": ".sql", "impact": 0.9, "path": "migrations/"},
        {"ext": ".yaml", "impact": 0.7, "path": "config/"}
    ],
    "Frontend": [
        {"ext": ".tsx", "impact": 1.1, "path": "src/components/"},
        {"ext": ".css", "impact": 0.6, "path": "src/styles/"},
        {"ext": ".js", "impact": 1.0, "path": "src/utils/"},
        {"ext": ".json", "impact": 0.4, "path": "public/"}
    ],
    "DevOps": [
        {"ext": ".yml", "impact": 1.3, "path": ".github/workflows/"},
        {"ext": ".tf", "impact": 1.2, "path": "infrastructure/"},
        {"ext": ".sh", "impact": 1.0, "path": "scripts/"},
        {"ext": ".dockerfile", "impact": 1.1, "path": "docker/"}
    ],
    "QA": [
        {"ext": ".py", "impact": 0.8, "path": "tests/"},
        {"ext": ".js", "impact": 0.7, "path": "e2e/"},
        {"ext": ".md", "impact": 0.3, "path": "docs/"},
        {"ext": ".json", "impact": 0.5, "path": "test-data/"}
    ]
}

def calculate_shannon_entropy(file_changes):
    """
    Calculate Shannon entropy based on distribution of effort across files
    H(X) = -Σ(Pi * log2(Pi))
    where Pi = (additions + deletions for file i) / total changes
    """
    if not file_changes:
        return 0.0
    
    # Calculate total changes across all files
    total_changes = sum(changes for changes in file_changes.values())
    
    if total_changes == 0:
        return 0.0
    
    # Calculate entropy
    entropy = 0.0
    for file_path, changes in file_changes.items():
        if changes > 0:
            pi = changes / total_changes
            entropy -= pi * math.log2(pi)
    
    return entropy

def generate_commit_files(author, repo):
    """Generate realistic file changes for a commit"""
    team_files = file_types[author["team"]]
    
    # Determine number of files to change (1-5 files per commit)
    num_files = random.choices([1, 2, 3, 4, 5], weights=[40, 30, 20, 8, 2])[0]
    
    file_changes = {}
    
    for _ in range(num_files):
        f_info = random.choice(team_files)
        
        # Generate unique file name
        file_id = random.randint(1, 100)
        file_name = f"{f_info['path']}{repo}_{file_id}{f_info['ext']}"
        
        # Generate realistic changes per file
        base_productivity = {
            "Backend": 1.2, "Frontend": 1.0, "DevOps": 1.4, "QA": 0.8
        }
        
        productivity_multiplier = base_productivity[author["team"]]
        individual_multiplier = random.uniform(0.7, 1.5)
        
        additions = int(random.randint(5, 80) * productivity_multiplier * individual_multiplier)
        deletions = int(random.randint(0, 40) * productivity_multiplier * individual_multiplier)
        
        total_changes = additions + deletions
        file_changes[file_name] = total_changes
    
    return file_changes

commits = []

for i in range(1, NUM_COMMITS + 1):
    author = random.choice(team_members)
    repo = random.choice(repos)
    
    # Generate file changes for this commit
    file_changes = generate_commit_files(author, repo)
    
    # Calculate Shannon entropy based on file distribution
    entropy = calculate_shannon_entropy(file_changes)
    
    # Calculate total additions and deletions
    total_additions = 0
    total_deletions = 0
    
    for file_path, total_changes in file_changes.items():
        # Distribute total changes between additions and deletions (roughly 70/30 split)
        file_additions = int(total_changes * random.uniform(0.6, 0.8))
        file_deletions = total_changes - file_additions
        
        total_additions += file_additions
        total_deletions += file_deletions
    
    commit = {
        "sha": f"sha_exec_{i:05}",
        "node_id": f"MDY6Q29tbWl0{i}",
        "commit": {
            "author": {
                "name": author["name"],
                "email": f"{author['name'].lower().replace(' ', '.')}@company.com",
                "date": (start_time + timedelta(hours=i * 0.5)).isoformat() + "Z"
            },
            "message": f"Update {len(file_changes)} files in {repo}",
            "comment_count": random.randint(0, 3)
        },
        "url": f"https://api.github.com/repos/org/{repo}/commits/sha_{i}",
        "files": [
            {
                "filename": file_path,
                "additions": int(total_changes * random.uniform(0.6, 0.8)),
                "deletions": total_changes - int(total_changes * random.uniform(0.6, 0.8)),
                "changes": total_changes
            }
            for file_path, total_changes in file_changes.items()
        ],
        # CUSTOM FIELDS for DevLens Engine
        "devlens_meta": {
            "teams_user_id": author["id"],  # THE JOIN KEY
            "team": author["team"],
            "files_changed": len(file_changes),
            "file_distribution": file_changes,
            "stats": {
                "additions": total_additions,
                "deletions": total_deletions,
                "total_entropy": entropy  # Shannon entropy based on file distribution
            }
        }
    }
    
    commits.append(commit)

output_path = "../data/exec_mock_data.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(commits, f, indent=2)

print(f"Generated {NUM_COMMITS} GitHub commits for {NUM_USERS} team members across 4 teams")
print(f"Shannon entropy calculated based on distribution of effort across files")
print(f"Sample entropy values: {[c['devlens_meta']['stats']['total_entropy'] for c in commits[:5]]}")