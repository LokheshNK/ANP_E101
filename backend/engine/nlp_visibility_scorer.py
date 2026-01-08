"""
Advanced NLP-based Visibility Scorer for DevLens
Analyzes message content using AI/NLP techniques to determine visibility scores
"""

import re
import json
import numpy as np
from typing import List, Dict, Union, Tuple
from collections import Counter
import math

class NLPVisibilityScorer:
    """
    Advanced NLP engine for calculating visibility scores from message content.
    Uses multiple AI/NLP techniques to analyze communication patterns and impact.
    """
    
    def __init__(self):
        # Technical impact keywords with weights
        self.technical_keywords = {
            "critical": 3.0, "urgent": 2.8, "blocker": 3.0, "security": 2.9,
            "performance": 2.5, "optimization": 2.3, "refactor": 2.4, "architecture": 2.6,
            "bug": 2.0, "fix": 1.8, "patch": 1.9, "hotfix": 2.2,
            "deploy": 2.1, "release": 2.0, "production": 2.3, "staging": 1.7,
            "api": 1.9, "database": 2.0, "migration": 2.2, "schema": 2.1,
            "test": 1.5, "testing": 1.5, "qa": 1.6, "automation": 1.8,
            "ci": 1.7, "cd": 1.7, "pipeline": 1.8, "build": 1.6,
            "feature": 1.4, "enhancement": 1.5, "improvement": 1.6,
            "review": 1.3, "merge": 1.4, "pr": 1.5, "pull request": 1.5
        }
        
        # Leadership and influence indicators
        self.leadership_keywords = {
            "decision": 2.5, "strategy": 2.8, "planning": 2.2, "roadmap": 2.4,
            "proposal": 2.0, "recommend": 1.8, "suggest": 1.6, "advise": 1.9,
            "lead": 2.3, "coordinate": 2.0, "organize": 1.8, "manage": 2.1,
            "delegate": 2.2, "assign": 1.7, "prioritize": 2.0, "schedule": 1.6,
            "meeting": 1.4, "discussion": 1.5, "alignment": 1.8, "consensus": 2.0
        }
        
        # Knowledge sharing and mentoring
        self.knowledge_sharing_keywords = {
            "explain": 1.8, "tutorial": 2.2, "guide": 2.0, "documentation": 2.1,
            "example": 1.6, "demo": 1.7, "walkthrough": 1.9, "training": 2.0,
            "mentor": 2.3, "teach": 2.1, "learn": 1.5, "onboard": 2.0,
            "best practice": 2.4, "pattern": 1.8, "standard": 1.9, "convention": 1.7,
            "tip": 1.4, "trick": 1.5, "hack": 1.6, "solution": 1.9
        }
        
        # Problem-solving and support
        self.problem_solving_keywords = {
            "help": 1.6, "support": 1.7, "assist": 1.5, "troubleshoot": 2.0,
            "debug": 1.9, "investigate": 1.8, "analyze": 1.7, "diagnose": 1.9,
            "resolve": 2.0, "solve": 1.9, "workaround": 1.7, "alternative": 1.6,
            "issue": 1.4, "problem": 1.5, "challenge": 1.6, "obstacle": 1.7,
            "blocker": 2.2, "stuck": 1.8, "confused": 1.5, "unclear": 1.4
        }
        
        # Collaboration and team engagement
        self.collaboration_keywords = {
            "team": 1.5, "together": 1.6, "collaborate": 1.8, "partnership": 1.9,
            "sync": 1.4, "align": 1.6, "coordinate": 1.7, "integrate": 1.8,
            "feedback": 1.7, "input": 1.5, "opinion": 1.4, "thoughts": 1.3,
            "agree": 1.2, "disagree": 1.4, "concern": 1.6, "question": 1.3,
            "clarify": 1.5, "confirm": 1.4, "verify": 1.5, "validate": 1.6
        }
        
        # Sentiment indicators
        self.positive_sentiment = {
            "great": 1.3, "excellent": 1.5, "awesome": 1.4, "perfect": 1.6,
            "thanks": 1.2, "appreciate": 1.4, "helpful": 1.5, "useful": 1.3,
            "good": 1.1, "nice": 1.1, "cool": 1.0, "amazing": 1.4,
            "love": 1.2, "like": 1.0, "enjoy": 1.1, "excited": 1.3
        }
        
        self.negative_sentiment = {
            "issue": 0.8, "problem": 0.7, "error": 0.6, "fail": 0.5,
            "broken": 0.4, "bug": 0.6, "wrong": 0.7, "bad": 0.6,
            "terrible": 0.3, "awful": 0.3, "hate": 0.2, "frustrated": 0.5,
            "confused": 0.6, "stuck": 0.5, "difficult": 0.7, "hard": 0.8
        }
        
        # Urgency and priority indicators
        self.urgency_patterns = [
            (r'\basap\b', 2.5), (r'\burgent\b', 2.8), (r'\bcritical\b', 3.0),
            (r'\bemergency\b', 3.2), (r'\bimmediate\b', 2.9), (r'\bnow\b', 2.0),
            (r'\btoday\b', 1.8), (r'\bquickly\b', 1.9), (r'\bfast\b', 1.7),
            (r'!!+', 2.2), (r'URGENT', 2.8), (r'CRITICAL', 3.0)
        ]
        
        # Question patterns (indicate engagement and knowledge seeking)
        self.question_patterns = [
            (r'\?', 1.2), (r'\bhow\s+to\b', 1.5), (r'\bwhat\s+if\b', 1.4),
            (r'\bwhy\s+', 1.3), (r'\bwhen\s+', 1.2), (r'\bwhere\s+', 1.1),
            (r'\bcan\s+you\b', 1.4), (r'\bcould\s+you\b', 1.3), (r'\bwould\s+you\b', 1.2)
        ]

    def extract_semantic_features(self, message: str) -> Dict[str, float]:
        """
        Extract semantic features from message content using NLP techniques.
        
        Args:
            message (str): Message content to analyze
            
        Returns:
            Dict[str, float]: Dictionary of semantic features and their scores
        """
        if not message or not isinstance(message, str):
            return {}
        
        message_lower = message.lower()
        features = {}
        
        # 1. Technical Impact Score
        technical_score = 0.0
        for keyword, weight in self.technical_keywords.items():
            if re.search(rf'\b{re.escape(keyword)}\b', message_lower):
                technical_score += weight
        features['technical_impact'] = min(technical_score, 10.0)  # Cap at 10
        
        # 2. Leadership and Influence Score
        leadership_score = 0.0
        for keyword, weight in self.leadership_keywords.items():
            if re.search(rf'\b{re.escape(keyword)}\b', message_lower):
                leadership_score += weight
        features['leadership_influence'] = min(leadership_score, 8.0)
        
        # 3. Knowledge Sharing Score
        knowledge_score = 0.0
        for keyword, weight in self.knowledge_sharing_keywords.items():
            if re.search(rf'\b{re.escape(keyword)}\b', message_lower):
                knowledge_score += weight
        
        # Bonus for code sharing
        if '```' in message or re.search(r'`[^`]+`', message):
            knowledge_score += 2.0
        
        # Bonus for links (documentation, resources)
        if re.search(r'https?://', message):
            knowledge_score += 1.5
        
        features['knowledge_sharing'] = min(knowledge_score, 8.0)
        
        # 4. Problem Solving Score
        problem_solving_score = 0.0
        for keyword, weight in self.problem_solving_keywords.items():
            if re.search(rf'\b{re.escape(keyword)}\b', message_lower):
                problem_solving_score += weight
        features['problem_solving'] = min(problem_solving_score, 6.0)
        
        # 5. Collaboration Score
        collaboration_score = 0.0
        for keyword, weight in self.collaboration_keywords.items():
            if re.search(rf'\b{re.escape(keyword)}\b', message_lower):
                collaboration_score += weight
        
        # Bonus for @mentions (direct collaboration)
        mention_count = len(re.findall(r'@\w+', message))
        collaboration_score += mention_count * 0.8
        
        features['collaboration'] = min(collaboration_score, 6.0)
        
        # 6. Sentiment Analysis
        positive_score = 0.0
        negative_score = 0.0
        
        for keyword, weight in self.positive_sentiment.items():
            if re.search(rf'\b{re.escape(keyword)}\b', message_lower):
                positive_score += weight
        
        for keyword, weight in self.negative_sentiment.items():
            if re.search(rf'\b{re.escape(keyword)}\b', message_lower):
                negative_score += weight
        
        # Net sentiment (positive - negative, normalized)
        net_sentiment = positive_score - negative_score
        features['sentiment_score'] = max(-2.0, min(2.0, net_sentiment))
        
        # 7. Urgency and Priority Score
        urgency_score = 0.0
        for pattern, weight in self.urgency_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                urgency_score += weight
        features['urgency_priority'] = min(urgency_score, 5.0)
        
        # 8. Engagement and Question Score
        engagement_score = 0.0
        for pattern, weight in self.question_patterns:
            matches = len(re.findall(pattern, message_lower))
            engagement_score += matches * weight
        features['engagement_questions'] = min(engagement_score, 4.0)
        
        # 9. Message Quality Indicators
        word_count = len(message.split())
        char_count = len(message)
        
        # Quality based on length and structure
        if word_count < 3:
            quality_score = 0.2
        elif word_count < 10:
            quality_score = 0.5
        elif word_count < 50:
            quality_score = 1.0
        elif word_count < 150:
            quality_score = 1.2  # Sweet spot
        elif word_count < 300:
            quality_score = 1.0
        else:
            quality_score = 0.8  # Too verbose
        
        # Bonus for structured content
        if re.search(r'^\s*[-*]\s+', message, re.MULTILINE):  # Bullet points
            quality_score += 0.3
        if re.search(r'^\s*\d+\.\s+', message, re.MULTILINE):  # Numbered lists
            quality_score += 0.3
        
        features['message_quality'] = quality_score
        
        return features

    def calculate_visibility_score(self, messages: Union[List[str], List[Dict], str], meeting_hours: float = 0.0) -> Dict[str, float]:
        """
        Calculate comprehensive visibility score using NLP analysis and meeting hours.
        
        Args:
            messages: List of messages or single message (string/dict format)
            meeting_hours: Number of meeting hours attended (default: 0.0)
            
        Returns:
            Dict containing visibility score and component breakdowns
        """
        # Normalize input to list of strings
        normalized_messages = self._normalize_messages(messages)
        
        if not normalized_messages and meeting_hours == 0.0:
            return {
                'visibility_score': 0.0,
                'component_scores': {},
                'message_count': 0,
                'meeting_hours': 0.0,
                'analysis_summary': 'No messages or meeting hours to analyze'
            }
        
        # Analyze each message
        all_features = []
        for message in normalized_messages:
            features = self.extract_semantic_features(message)
            if features:  # Only add non-empty feature sets
                all_features.append(features)
        
        # If no message features but have meeting hours, create minimal feature set
        if not all_features and meeting_hours > 0:
            all_features = [{'message_quality': 0.5}]  # Minimal quality for meeting-only visibility
        
        if not all_features:
            return {
                'visibility_score': 0.0,
                'component_scores': {},
                'message_count': len(normalized_messages),
                'meeting_hours': meeting_hours,
                'analysis_summary': 'No analyzable content found'
            }
        
        # Aggregate features across all messages
        aggregated_features = self._aggregate_features(all_features)
        
        # Calculate meeting engagement score
        meeting_engagement = self._calculate_meeting_engagement(meeting_hours)
        
        # Calculate component scores with weights (adjusted for meeting hours)
        component_weights = {
            'technical_impact': 0.25,       # 25% - Technical contributions
            'leadership_influence': 0.20,   # 20% - Leadership and decision making
            'knowledge_sharing': 0.20,      # 20% - Teaching and documentation
            'problem_solving': 0.15,        # 15% - Helping others
            'collaboration': 0.10,          # 10% - Team engagement
            'meeting_engagement': 0.08,     # 8% - Meeting participation (reduced)
            'urgency_priority': 0.01,       # 1% - Handling urgent matters
            'engagement_questions': 0.01    # 1% - Active participation
        }
        
        # Calculate weighted visibility score
        visibility_score = 0.0
        component_scores = {}
        
        # Check if we have meaningful communication content
        has_meaningful_communication = len(normalized_messages) > 0 and any(
            len(msg.strip()) > 10 for msg in normalized_messages
        )
        
        for component, weight in component_weights.items():
            if component == 'meeting_engagement':
                component_score = meeting_engagement
                # Apply communication penalty to meeting engagement
                if not has_meaningful_communication:
                    component_score *= 0.3  # Reduce meeting score by 70% if no meaningful communication
            else:
                component_score = aggregated_features.get(component, 0.0)
            
            component_scores[component] = component_score
            visibility_score += component_score * weight
        
        # Apply communication requirement multiplier
        if not has_meaningful_communication:
            # Severe penalty for no communication - meetings alone shouldn't give high visibility
            communication_penalty = 0.2  # Maximum 20% of full score without communication
            visibility_score *= communication_penalty
        
        # Apply message quality multiplier (only if we have messages)
        if normalized_messages:
            quality_multiplier = aggregated_features.get('message_quality', 1.0)
            visibility_score *= quality_multiplier
        else:
            quality_multiplier = 1.0
        
        # Apply sentiment adjustment (only if we have messages)
        if normalized_messages:
            sentiment_score = aggregated_features.get('sentiment_score', 0.0)
            sentiment_multiplier = 1.0 + (sentiment_score * 0.1)  # ±20% max adjustment
            visibility_score *= sentiment_multiplier
        else:
            sentiment_multiplier = 1.0
        
        # Apply frequency factor for messages (optimal range: 5-30 messages)
        message_count = len(normalized_messages)
        if message_count == 0:
            frequency_factor = 0.8  # Slight penalty for no messages, but meeting hours can compensate
        elif message_count < 5:
            frequency_factor = 0.8 + (message_count / 5.0) * 0.2  # Gradual improvement
        elif message_count <= 30:
            frequency_factor = 1.0  # Optimal range
        else:
            frequency_factor = max(0.7, 1.0 - (message_count - 30) * 0.01)  # Slight penalty for spam
        
        visibility_score *= frequency_factor
        
        # Normalize to 0-10 scale
        visibility_score = min(10.0, max(0.0, visibility_score))
        
        return {
            'visibility_score': round(visibility_score, 2),
            'component_scores': {k: round(v, 2) for k, v in component_scores.items()},
            'message_count': message_count,
            'meeting_hours': meeting_hours,
            'meeting_engagement': round(meeting_engagement, 2),
            'has_meaningful_communication': has_meaningful_communication,
            'communication_penalty_applied': not has_meaningful_communication,
            'quality_multiplier': round(quality_multiplier, 2),
            'sentiment_multiplier': round(sentiment_multiplier, 2),
            'frequency_factor': round(frequency_factor, 2),
            'analysis_summary': self._generate_analysis_summary(component_scores, visibility_score, has_meaningful_communication)
        }

    def _normalize_messages(self, messages: Union[List[str], List[Dict], str]) -> List[str]:
        """Normalize different message formats to list of strings."""
        if isinstance(messages, str):
            try:
                # Try to parse as JSON first
                parsed = json.loads(messages)
                if isinstance(parsed, list):
                    messages = parsed
                else:
                    return [messages]
            except (json.JSONDecodeError, TypeError):
                return [messages]
        
        if not isinstance(messages, list):
            return []
        
        normalized = []
        for msg in messages:
            if isinstance(msg, str):
                if msg.strip():  # Only add non-empty messages
                    normalized.append(msg.strip())
            elif isinstance(msg, dict):
                # Extract content from various possible fields
                content = (msg.get('text') or msg.get('content') or 
                          msg.get('message') or msg.get('body', {}).get('content', ''))
                if content and isinstance(content, str) and content.strip():
                    normalized.append(content.strip())
        
        return normalized

    def _aggregate_features(self, all_features: List[Dict[str, float]]) -> Dict[str, float]:
        """Aggregate features across all messages."""
        if not all_features:
            return {}
        
        aggregated = {}
        feature_keys = set()
        for features in all_features:
            feature_keys.update(features.keys())
        
        for key in feature_keys:
            values = [features.get(key, 0.0) for features in all_features]
            
            # Use different aggregation strategies for different features
            if key in ['sentiment_score']:
                # Average for sentiment
                aggregated[key] = sum(values) / len(values)
            elif key in ['message_quality']:
                # Average for quality
                aggregated[key] = sum(values) / len(values)
            else:
                # Sum for most features (represents total contribution)
                aggregated[key] = sum(values)
        
        return aggregated

    def _calculate_meeting_engagement(self, meeting_hours: float) -> float:
        """
        Calculate meeting engagement score based on meeting hours attended.
        
        Args:
            meeting_hours (float): Number of meeting hours attended
            
        Returns:
            float: Meeting engagement score (0-100)
        """
        if meeting_hours <= 0:
            return 0.0
        elif meeting_hours <= 2.0:
            return meeting_hours * 20.0  # 0-40 points for minimal meeting time
        elif meeting_hours <= 8.0:
            return 40.0 + (meeting_hours - 2.0) * 8.0  # 40-88 points for moderate meeting time
        elif meeting_hours <= 15.0:
            return 88.0 + (meeting_hours - 8.0) * 1.5  # 88-98.5 points for good meeting time
        elif meeting_hours <= 25.0:
            return min(100.0, 98.5 + (meeting_hours - 15.0) * 0.15)  # Approach 100 for high meeting time
        else:
            # Penalty for excessive meeting hours (meeting overload)
            return max(75.0, 100.0 - (meeting_hours - 25.0) * 2.0)

    def _generate_analysis_summary(self, component_scores: Dict[str, float], visibility_score: float, has_meaningful_communication: bool = True) -> str:
        """Generate human-readable analysis summary."""
        if not has_meaningful_communication:
            return f"Low visibility ({visibility_score:.1f}/10) - Meeting attendance without meaningful communication"
        
        if visibility_score >= 8.0:
            level = "Exceptional"
        elif visibility_score >= 6.0:
            level = "High"
        elif visibility_score >= 4.0:
            level = "Moderate"
        elif visibility_score >= 2.0:
            level = "Low"
        else:
            level = "Minimal"
        
        # Find top contributing components
        sorted_components = sorted(component_scores.items(), key=lambda x: x[1], reverse=True)
        top_components = [comp[0].replace('_', ' ').title() for comp in sorted_components[:2] if comp[1] > 0]
        
        summary = f"{level} visibility ({visibility_score}/10)"
        if top_components:
            summary += f" - Strong in: {', '.join(top_components)}"
        
        return summary

# Convenience function for easy integration
def analyze_message_visibility(messages: Union[List[str], List[Dict], str], meeting_hours: float = 0.0) -> Dict[str, float]:
    """
    Convenience function to analyze message visibility using NLP and meeting hours.
    
    Args:
        messages: Messages to analyze (various formats supported)
        meeting_hours: Number of meeting hours attended (default: 0.0)
        
    Returns:
        Dict containing visibility analysis results
    """
    scorer = NLPVisibilityScorer()
    return scorer.calculate_visibility_score(messages, meeting_hours)