import re
import json
import numpy as np

class TechFilter:
    def __init__(self):
        self.tech_weights = {
            "auth": 2.0, "bug": 1.5, "refactor": 2.5, "db": 2.0,
            "pr": 1.5, "api": 1.8, "fix": 1.2, "logic": 2.0,
            "ci": 1.5, "cd": 1.5, "test": 1.0, "deploy": 2.0,
            "merge": 1.3, "feature": 1.5, "update": 1.0, "add": 0.8,
            "remove": 1.0, "delete": 1.0, "create": 1.2, "implement": 1.8,
            "optimize": 2.0, "performance": 1.8, "security": 2.2,
            "config": 1.5, "setup": 1.3, "install": 1.0, "upgrade": 1.5
        }
        
    def clean_text(self, raw_html):
        """Strips HTML and prepares text for keyword analysis."""
        if not raw_html: return ""
        # 1. Remove HTML tags
        clean = re.sub('<[^<]+?>', '', raw_html)
        return clean.lower().strip()

    def get_technical_score(self, text):
        """Calculates a weighted score based on keyword presence."""
        score = 0.0
        clean = self.clean_text(text)
        
        for word, weight in self.tech_weights.items():
            # \b ensures we match 'api' but NOT 'tapioca'
            if re.search(rf'\b{word}\b', clean):
                score += weight
                
        if "http" in clean or "github.com" in clean:
            score += 1.5
            
        return score

def analyze_communication(messages_json):
    """
    Advanced analysis of communication data (Slack messages) with sophisticated scoring
    
    This function analyzes:
    1. Message Quality vs Quantity
    2. Technical Relevance and Depth
    3. Collaboration Patterns
    4. Knowledge Sharing Indicators
    
    Args:
        messages_json (str or list): JSON string containing Slack messages OR list of message strings
        
    Returns:
        float: Sophisticated communication score
    """
    # Handle different input formats
    messages = []
    
    if isinstance(messages_json, str):
        try:
            messages = json.loads(messages_json)
            if not isinstance(messages, list):
                return 0.0
        except (json.JSONDecodeError, TypeError):
            return 0.0
    elif isinstance(messages_json, list):
        messages = messages_json
    else:
        return 0.0
    
    if len(messages) == 0:
        return 0.0
    
    filter_engine = TechFilter()
    
    # Initialize scoring components
    total_technical_score = 0.0
    total_collaboration_score = 0.0
    total_knowledge_sharing_score = 0.0
    total_engagement_score = 0.0
    
    message_count = len(messages)
    
    # Collaboration indicators
    collaboration_keywords = [
        'help', 'support', 'assist', 'collaborate', 'team', 'together',
        'pair', 'review', 'feedback', 'suggest', 'recommend', 'share'
    ]
    
    # Knowledge sharing indicators
    knowledge_keywords = [
        'explain', 'tutorial', 'guide', 'documentation', 'learn', 'teach',
        'example', 'demo', 'walkthrough', 'best practice', 'tip', 'trick'
    ]
    
    # Question/engagement indicators
    engagement_patterns = [
        r'\?',  # Questions
        r'how to',  # Help seeking
        r'what if',  # Scenario exploration
        r'why',  # Understanding seeking
        r'thanks?|thank you',  # Gratitude (indicates helpful behavior)
        r'great|awesome|excellent',  # Positive feedback
    ]
    
    for message in messages:
        # Extract message content - handle both string and dict formats
        content = ""
        if isinstance(message, dict):
            content = message.get('text', '') or message.get('content', '') or message.get('message', '') or message.get('body', {}).get('content', '')
        elif isinstance(message, str):
            content = message
        
        if not content:
            continue
        
        content_lower = content.lower()
        
        # 1. Technical Relevance Score
        tech_score = filter_engine.get_technical_score(content)
        
        # 2. Message Quality Analysis
        length = len(content)
        
        # Quality based on message length and structure
        if length < 10:
            quality_multiplier = 0.3  # Very short messages (low quality)
        elif length < 50:
            quality_multiplier = 0.7  # Short messages
        elif length < 200:
            quality_multiplier = 1.0  # Good length messages
        elif length < 500:
            quality_multiplier = 1.2  # Detailed messages (bonus)
        else:
            quality_multiplier = 1.0  # Very long (might be verbose)
        
        # 3. Collaboration Score
        collaboration_score = 0.0
        for keyword in collaboration_keywords:
            if keyword in content_lower:
                collaboration_score += 0.5
        
        # Bonus for @mentions (indicates direct collaboration)
        if '@' in content:
            collaboration_score += 1.0
        
        # 4. Knowledge Sharing Score
        knowledge_score = 0.0
        for keyword in knowledge_keywords:
            if keyword in content_lower:
                knowledge_score += 0.7
        
        # Bonus for sharing links/resources
        if 'http' in content or 'github' in content or 'docs' in content_lower:
            knowledge_score += 1.0
        
        # 5. Engagement Score
        engagement_score = 0.0
        for pattern in engagement_patterns:
            if re.search(pattern, content_lower):
                engagement_score += 0.5
        
        # Code sharing bonus (indicates technical knowledge sharing)
        if '```' in content or '`' in content:
            tech_score += 1.5
            knowledge_score += 1.0
        
        # Apply quality multiplier to all scores
        total_technical_score += tech_score * quality_multiplier
        total_collaboration_score += collaboration_score * quality_multiplier
        total_knowledge_sharing_score += knowledge_score * quality_multiplier
        total_engagement_score += engagement_score * quality_multiplier
    
    # Calculate component averages
    avg_technical = total_technical_score / message_count
    avg_collaboration = total_collaboration_score / message_count
    avg_knowledge = total_knowledge_sharing_score / message_count
    avg_engagement = total_engagement_score / message_count
    
    # Base participation score
    participation_score = min(3.0, np.log1p(message_count))
    
    # Frequency analysis
    # Optimal range: 10-50 messages per period
    if message_count < 5:
        frequency_multiplier = 0.5  # Too quiet
    elif message_count <= 50:
        frequency_multiplier = 1.0 + (message_count / 100.0)  # Good participation
    elif message_count <= 100:
        frequency_multiplier = 1.3  # High participation
    else:
        frequency_multiplier = 1.1  # Very high (might be spam)
    
    # Combine all components with weights
    final_score = (
        avg_technical * 0.3 +        # 30% technical relevance
        avg_collaboration * 0.25 +   # 25% collaboration
        avg_knowledge * 0.25 +       # 25% knowledge sharing
        avg_engagement * 0.2         # 20% engagement
    ) * participation_score * frequency_multiplier
    
    # Quality bonus for well-rounded communicators
    component_count = sum(1 for score in [avg_technical, avg_collaboration, avg_knowledge, avg_engagement] if score > 0.5)
    if component_count >= 3:
        final_score *= 1.2  # 20% bonus for being strong in multiple areas
    
    return round(final_score, 2)