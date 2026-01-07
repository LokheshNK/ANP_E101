# Technical Keywords used to weight the communication score
TECH_KEYWORDS = [
    'refactor', 'bug', 'fix', 'pr', 'merge', 'latency', 'deploy', 
    'api', 'schema', 'logic', 'endpoint', 'hotfix', 'async', 'db'
]

def analyze_communication(messages):
    """
    Parses a list of messages to calculate a weighted Communication Score.
    This ensures that 1 technical message > 10 social messages.
    """
    total_score = 0
    for msg in messages:
        msg_lower = msg.lower()
        
        # Base weight for any interaction
        weight = 0.5 
        
        # Technical Signal Bonus (Keyword Matching)
        if any(key in msg_lower for key in TECH_KEYWORDS):
            weight = 1.5
            
        # Link/Execution Bonus (Contextual Evidence)
        if "github.com" in msg_lower or "jira" in msg_lower or "pr" in msg_lower:
            weight += 1.0
            
        total_score += weight
    return total_score