import json
import pandas as pd
import numpy as np
from .nlp_filter import TechFilter
from .nlp_visibility_scorer import NLPVisibilityScorer

class DevLensKeywordScorer:
    def __init__(self, developers_data=None):
        """
        Initialize scorer with developer data from database
        
        Args:
            developers_data (list): List of developer dictionaries from database
        """
        self.developers_data = developers_data or []
        self.filter = TechFilter()
        self.nlp_visibility_scorer = NLPVisibilityScorer()
        
        # Define our Keyword Weights
        self.tech_weights = {
            "auth": 2.0, "bug": 1.5, "refactor": 2.5, "db": 2.0,
            "pr": 1.5, "api": 1.8, "fix": 1.2, "logic": 2.0,
            "ci": 1.5, "cd": 1.5, "test": 1.0, "deploy": 2.0,
            "merge": 1.3, "feature": 1.5, "update": 1.0, "add": 0.8,
            "remove": 1.0, "delete": 1.0, "create": 1.2, "implement": 1.8,
            "optimize": 2.0, "performance": 1.8, "security": 2.2,
            "config": 1.5, "setup": 1.3, "install": 1.0, "upgrade": 1.5
        }

    def get_visibility_weight_from_messages(self, messages, meeting_hours=0.0):
        """
        Calculate visibility weight from messages using advanced NLP analysis and meeting hours
        
        Args:
            messages (list): List of message dictionaries
            meeting_hours (float): Number of meeting hours attended
            
        Returns:
            dict: Comprehensive visibility analysis including score and breakdown
        """
        if not messages and meeting_hours == 0.0:
            return {
                'visibility_score': 0.1,
                'nlp_analysis': {
                    'visibility_score': 0.0,
                    'component_scores': {},
                    'message_count': 0,
                    'meeting_hours': 0.0,
                    'analysis_summary': 'No messages or meeting hours to analyze'
                },
                'legacy_score': 0.1
            }
        
        # Use the new NLP visibility scorer for comprehensive analysis (including meeting hours)
        nlp_analysis = self.nlp_visibility_scorer.calculate_visibility_score(messages, meeting_hours)
        
        # Also calculate legacy score for comparison/fallback
        legacy_score = self._calculate_legacy_visibility_score(messages)
        
        # Combine NLP score with legacy approach (weighted average)
        # 80% NLP analysis, 20% legacy for stability
        combined_score = (nlp_analysis['visibility_score'] * 0.8) + (legacy_score * 0.2)
        
        return {
            'visibility_score': combined_score,
            'nlp_analysis': nlp_analysis,
            'legacy_score': legacy_score
        }

    def _calculate_legacy_visibility_score(self, messages):
        """
        Legacy visibility calculation method (for comparison and fallback)
        """
        total_weight = 0.0
        
        for message in messages:
            # Extract message content
            content = ""
            if isinstance(message, dict):
                content = message.get('text', '') or message.get('content', '') or message.get('message', '')
            elif isinstance(message, str):
                content = message
            
            if not content:
                continue
            
            # Base weight for any message
            weight = 0.5
            
            # Calculate technical weight
            clean_text = self.filter.clean_text(content)
            
            for word, bonus in self.tech_weights.items():
                if word in clean_text:
                    weight += bonus * 0.3  # Reduced multiplier for more balanced scoring
            
            if "http" in content or "github" in content:
                weight += 0.8
            
            total_weight += weight
        
        # Scale down visibility to create better distribution
        return total_weight * 0.3

    def calculate_sophisticated_impact_from_commits(self, commits, entropy):
        """
        Calculate sophisticated impact score from commit data with better scaling
        
        Args:
            commits (int): Number of commits
            entropy (float): Total entropy from database
            
        Returns:
            float: Sophisticated impact score
        """
        if commits == 0:
            return 0.1  # Minimum impact for no commits
        
        # Calculate average entropy per commit
        avg_entropy = entropy / commits
        
        # Enhanced impact calculation
        # Base impact from commits (logarithmic scaling)
        commit_impact = np.log1p(commits) * 0.5
        
        # Entropy impact (complexity/quality indicator)
        entropy_impact = avg_entropy * 2.0
        
        # Bonus for high-entropy, high-commit developers
        if commits >= 15 and avg_entropy >= 0.7:
            bonus = 1.0
        elif commits >= 10 and avg_entropy >= 0.5:
            bonus = 0.5
        else:
            bonus = 0.0
        
        # Penalty for micro-commits
        if avg_entropy < 0.2:
            penalty = 0.5
        else:
            penalty = 1.0
        
        # Final impact score
        impact_score = (commit_impact + entropy_impact + bonus) * penalty
        
        return max(0.1, impact_score)  # Ensure minimum impact

    def calculate_meeting_engagement_score(self, meetings):
        """
        Calculate meeting engagement score with optimal range detection
        
        Args:
            meetings (int): Number of meetings attended
            
        Returns:
            dict: Meeting score and quality assessment
        """
        if meetings == 0:
            return {"score": 0.1, "quality": "Poor - No Meetings"}
        elif meetings <= 5:
            return {"score": meetings * 0.15, "quality": "Low Engagement"}
        elif meetings <= 15:
            return {"score": 1.0 + (meetings - 6) * 0.05, "quality": "Good Balance"}
        elif meetings <= 25:
            return {"score": 1.2 - (meetings - 15) * 0.02, "quality": "High Engagement"}
        else:
            return {"score": 0.8 - (meetings - 25) * 0.01, "quality": "Meeting Overload"}

    def calculate_scores_from_database(self):
        """
        Calculate scores using database developer data with proper quadrant analysis
        
        Returns:
            dict: Processed results with scores, statistics, and quadrant classifications
        """
        if not self.developers_data:
            return {}
        
        results = {}
        detailed_stats = {}
        
        for dev in self.developers_data:
            dev_id = f"dev_{dev['name'].replace(' ', '_').lower()}"
            
            # Extract data from database
            commits = dev.get('commits', 0)
            entropy = dev.get('entropy', 0.0)
            meetings = dev.get('meetings', 0)
            messages = dev.get('msgs', [])
            
            # Calculate visibility from communication using NLP analysis (including meeting hours)
            meeting_hours = meetings * 1.5  # Assume 1.5 hours per meeting on average
            visibility_analysis = self.get_visibility_weight_from_messages(messages, meeting_hours)
            visibility_weight = visibility_analysis['visibility_score']
            
            # Calculate impact from commits and entropy
            impact_score = self.calculate_sophisticated_impact_from_commits(commits, entropy)
            
            # Calculate meeting engagement
            meeting_data = self.calculate_meeting_engagement_score(meetings)
            
            # Store detailed statistics including NLP analysis
            detailed_stats[dev_id] = {
                'total_commits': commits,
                'total_entropy': entropy,
                'avg_entropy_per_commit': entropy / max(1, commits),
                'total_meetings': meetings,
                'total_messages': len(messages),
                'sophisticated_impact': impact_score,
                'meeting_engagement': meeting_data["score"],
                'meeting_quality': meeting_data["quality"],
                'visibility_weight': visibility_weight,
                'visibility_analysis': visibility_analysis,  # Include full NLP analysis
                'name': dev.get('name', 'Unknown'),
                'team': dev.get('team', 'Unknown')
            }
            
            # Store results for quadrant calculation
            results[dev_id] = {
                'visibility': visibility_weight,
                'impact': impact_score,
                'raw_data': dev
            }
        
        # Store detailed stats for API access
        self.detailed_stats = detailed_stats
        
        # Calculate quadrants with proper normalization
        if len(results) > 1:
            # Extract values for normalization
            visibilities = [r['visibility'] for r in results.values()]
            impacts = [r['impact'] for r in results.values()]
            
            # Calculate medians for quadrant boundaries
            visibility_median = np.median(visibilities)
            impact_median = np.median(impacts)
            
            # Create DataFrame for processing
            df = pd.DataFrame({
                'visibility': visibilities,
                'impact': impacts
            }, index=list(results.keys()))
            
            # Ensure variance (add small noise if needed)
            if df['visibility'].std() == 0:
                df['visibility'] = df['visibility'] + np.random.normal(0, 0.1, len(df))
            if df['impact'].std() == 0:
                df['impact'] = df['impact'] + np.random.normal(0, 0.1, len(df))
            
            # Log transform for better distribution
            df['x_log'] = np.log1p(df['visibility'])
            df['y_log'] = np.log1p(df['impact'])
            
            # Z-score normalization for scatter plot positioning
            x_std = df['x_log'].std() if df['x_log'].std() > 0 else 1.0
            y_std = df['y_log'].std() if df['y_log'].std() > 0 else 1.0
            
            df['x_final'] = (df['x_log'] - df['x_log'].mean()) / x_std
            df['y_final'] = (df['y_log'] - df['y_log'].mean()) / y_std
            
            # Calculate quadrants based on raw scores (not normalized)
            for dev_id in results.keys():
                raw_visibility = results[dev_id]['visibility']
                raw_impact = results[dev_id]['impact']
                
                # Determine quadrant based on median thresholds
                if raw_impact >= impact_median and raw_visibility >= visibility_median:
                    quadrant = 1  # High Impact, High Visibility - "Stars"
                    quadrant_name = "Star Performer"
                elif raw_impact >= impact_median and raw_visibility < visibility_median:
                    quadrant = 2  # High Impact, Low Visibility - "Hidden Gems"
                    quadrant_name = "Hidden Gem"
                elif raw_impact < impact_median and raw_visibility >= visibility_median:
                    quadrant = 3  # Low Impact, High Visibility - "Communicators"
                    quadrant_name = "Team Connector"
                else:
                    quadrant = 4  # Low Impact, Low Visibility - "Needs Support"
                    quadrant_name = "Needs Support"
                
                results[dev_id].update({
                    'x_final': df.loc[dev_id, 'x_final'],
                    'y_final': df.loc[dev_id, 'y_final'],
                    'quadrant': quadrant,
                    'quadrant_name': quadrant_name,
                    'visibility_median': visibility_median,
                    'impact_median': impact_median
                })
        else:
            # Single developer case
            for dev_id in results.keys():
                results[dev_id].update({
                    'x_final': 0.0,
                    'y_final': 0.0,
                    'quadrant': 1,
                    'quadrant_name': "Star Performer",
                    'visibility_median': 0.0,
                    'impact_median': 0.0
                })
        
        return results

    def get_detailed_stats(self):
        """Return detailed execution statistics per person"""
        return getattr(self, 'detailed_stats', {})

    def get_team_info(self):
        """Extract team information from developer data"""
        team_info = {}
        
        for dev in self.developers_data:
            dev_id = f"dev_{dev['name'].replace(' ', '_').lower()}"
            team_info[dev_id] = {
                'name': dev.get('name', 'Unknown'),
                'team': dev.get('team', 'Unknown')
            }
        
        return team_info

def process_metrics(developers):
    """
    Advanced processing of developer metrics using sophisticated scoring algorithms
    Now includes attendance as a critical performance factor
    
    Args:
        developers (list): List of developer dictionaries from database
        
    Returns:
        list: Processed developers with calculated scores, quadrant classifications, and metrics
    """
    if not developers:
        return []
    
    # Initialize the scorer with database data
    scorer = DevLensKeywordScorer(developers)
    
    # Calculate scores using the sophisticated algorithm
    score_results = scorer.calculate_scores_from_database()
    detailed_stats = scorer.get_detailed_stats()
    
    processed_developers = []
    
    for dev in developers:
        dev_id = f"dev_{dev['name'].replace(' ', '_').lower()}"
        
        # Get calculated scores
        scores = score_results.get(dev_id, {})
        stats = detailed_stats.get(dev_id, {})
        
        # Extract basic metrics
        commits = dev.get('commits', 0)
        entropy = dev.get('entropy', 0.0)
        meetings = dev.get('meetings', 0)
        comm_score = dev.get('comm_score', 0.0)
        
        # Get attendance data (this will be added by main.py)
        attendance_rate = dev.get('attendance_rate', 0.85)  # Default 85% if not provided
        
        # Get sophisticated scores
        technical_impact = scores.get('impact', 0.0)
        visibility_score = scores.get('visibility', 0.0)
        quadrant = scores.get('quadrant', 4)
        quadrant_name = scores.get('quadrant_name', 'Needs Support')
        
        # CRITICAL: Calculate Attendance-Weighted Performance Score
        # This is the key fix - attendance must be a major factor in overall performance
        
        # 1. Attendance Factor (0.0 to 1.0)
        attendance_factor = max(0.1, attendance_rate)  # Minimum 10% to avoid zero scores
        
        # 2. Attendance Penalty for low attendance
        if attendance_rate < 0.7:  # Below 70% attendance
            attendance_penalty = 0.5  # 50% penalty
        elif attendance_rate < 0.8:  # Below 80% attendance  
            attendance_penalty = 0.7  # 30% penalty
        elif attendance_rate < 0.9:  # Below 90% attendance
            attendance_penalty = 0.85  # 15% penalty
        else:
            attendance_penalty = 1.0  # No penalty
        
        # 3. Calculate Attendance-Weighted Scores
        # Technical impact is heavily penalized by poor attendance
        adjusted_technical_impact = technical_impact * attendance_factor * attendance_penalty
        
        # Visibility is also affected but less severely (you can't be visible if you're not there)
        adjusted_visibility_score = visibility_score * (0.5 + 0.5 * attendance_factor)
        
        # 4. Overall Performance Score (this is what we'll use for ranking)
        # Formula: (Technical Impact * 0.4 + Visibility * 0.3 + Attendance * 0.3)
        overall_performance_score = (
            adjusted_technical_impact * 0.4 +  # 40% technical contribution
            adjusted_visibility_score * 0.3 +   # 30% team visibility  
            attendance_rate * 10 * 0.3          # 30% attendance (scaled to match other scores)
        )
        
        # 5. Calculate quadrant based on adjusted scores using simpler, more reliable logic
        # First, we need to collect all adjusted scores to calculate medians properly
        
        # Store this developer's adjusted scores for later quadrant calculation
        processed_dev = dev.copy()
        processed_dev.update({
            'adjusted_technical_impact': adjusted_technical_impact,
            'adjusted_visibility_score': adjusted_visibility_score,
            'overall_performance_score': overall_performance_score,
            'attendance_rate': attendance_rate,
            'attendance_factor': attendance_factor,
            'attendance_penalty': attendance_penalty,
            'raw_technical_impact': technical_impact,
            'raw_visibility_score': visibility_score,
            'commits': commits,
            'entropy': entropy,
            'meetings': meetings,
            'comm_score': comm_score
        })
        
        processed_developers.append(processed_dev)
    
    # Now calculate quadrants for all developers at once
    if len(processed_developers) > 1:
        # Calculate medians for quadrant boundaries
        impact_scores = [dev['adjusted_technical_impact'] for dev in processed_developers]
        visibility_scores = [dev['adjusted_visibility_score'] for dev in processed_developers]
        
        impact_median = np.median(impact_scores)
        visibility_median = np.median(visibility_scores)
        
        print(f"Debug: Impact median = {impact_median:.2f}, Visibility median = {visibility_median:.2f}")
        
        # Assign quadrants to each developer
        for dev in processed_developers:
            impact = dev['adjusted_technical_impact']
            visibility = dev['adjusted_visibility_score']
            attendance = dev['attendance_rate']
            
            # Determine quadrant based on median thresholds
            if impact >= impact_median and visibility >= visibility_median:
                quadrant = 1  # High Impact, High Visibility - "Stars"
                archetype = "Star Performer"
            elif impact >= impact_median and visibility < visibility_median:
                quadrant = 2  # High Impact, Low Visibility - "Hidden Gems"
                archetype = "Hidden Gem"
            elif impact < impact_median and visibility >= visibility_median:
                quadrant = 3  # Low Impact, High Visibility - "Communicators"
                archetype = "Team Connector"
            else:
                quadrant = 4  # Low Impact, Low Visibility - "Needs Support"
                archetype = "Needs Support"
            
            # Hidden Gem criteria: Quadrant 2 AND good attendance (>= 75%)
            is_hidden_gem = (quadrant == 2 and attendance >= 0.75)
            
            print(f"Debug: {dev['name']} - Impact: {impact:.2f}, Visibility: {visibility:.2f}, Quadrant: {quadrant}, Hidden Gem: {is_hidden_gem}")
            
            # 6. Additional attendance-based risk factors
            risk_factors = []
            if dev['commits'] == 0:
                risk_factors.append("No Code Contributions")
            if dev['comm_score'] == 0:
                risk_factors.append("No Communication")
            if dev['meetings'] == 0:
                risk_factors.append("No Meeting Attendance")
            if dev['commits'] > 0 and dev['entropy'] / dev['commits'] < 0.1:
                risk_factors.append("Potential Micro-commits")
            if dev['meetings'] > 30:
                risk_factors.append("Meeting Overload")
            
            # ATTENDANCE-SPECIFIC RISK FACTORS
            if attendance < 0.5:
                risk_factors.append("Critical Attendance Issue")
            elif attendance < 0.7:
                risk_factors.append("Poor Attendance")
            elif attendance < 0.8:
                risk_factors.append("Below Average Attendance")
            
            # Calculate additional metrics
            entropy_per_commit = dev['entropy'] / max(1, dev['commits'])
            commits_per_meeting = dev['commits'] / max(1, dev['meetings'])
            communication_efficiency = dev['comm_score'] / max(1, dev['meetings'])
            
            # Update developer with all calculated metrics
            dev.update({
                # Core scores (now attendance-adjusted)
                'impact_score': round(impact, 2),
                'visibility_score': round(visibility, 2),
                'overall_performance_score': round(dev['overall_performance_score'], 2),
                
                # Original scores (for reference)
                'raw_technical_impact': round(dev['raw_technical_impact'], 2),
                'raw_visibility_score': round(dev['raw_visibility_score'], 2),
                
                # Attendance metrics
                'attendance_factor': round(dev['attendance_factor'], 3),
                'attendance_penalty': round(dev['attendance_penalty'], 3),
                
                # Sophisticated metrics
                'technical_impact': round(impact, 2),
                'communication_impact': round(dev['comm_score'] * 1.5, 2),
                'meeting_score': round(0, 2),  # Placeholder
                
                # Quality indicators
                'entropy_per_commit': round(entropy_per_commit, 3),
                'meeting_quality': 'Unknown',
                
                # Performance metrics
                'archetype': archetype,
                'commits_per_meeting': round(commits_per_meeting, 2),
                'communication_efficiency': round(communication_efficiency, 2),
                
                # Risk assessment (now includes attendance risks)
                'risk_factors': risk_factors,
                'risk_level': 'High' if len(risk_factors) >= 3 else 'Medium' if len(risk_factors) >= 2 else 'Low',
                
                # Quadrant positioning (for scatter plot) - using adjusted scores
                'imp_z': (impact - impact_median) / (np.std(impact_scores) or 1.0),  # Z-score for plot
                'vis_z': (visibility - visibility_median) / (np.std(visibility_scores) or 1.0),
                'raw_impact': impact,  # Use adjusted scores for quadrant calculation
                'raw_visibility': visibility,
                
                # Quadrant classification
                'quadrant': quadrant,
                'quadrant_name': archetype,
                'is_hidden_gem': is_hidden_gem,  # This is the key field for frontend
                
                # Detailed quadrant description
                'quadrant_description': (
                    "High Impact, High Visibility - Star performers who deliver results and communicate well"
                    if quadrant == 1 else
                    "High Impact, Low Visibility - Hidden gems who deliver great work but need more recognition"
                    if quadrant == 2 else
                    "Low Impact, High Visibility - Great communicators who could focus more on technical delivery"
                    if quadrant == 3 else
                    "Low Impact, Low Visibility - Team members who need support and development"
                )
            })
    else:
        # Single developer case
        dev = processed_developers[0]
        dev.update({
            'quadrant': 1,
            'quadrant_name': "Star Performer",
            'is_hidden_gem': False,
            'imp_z': 0.0,
            'vis_z': 0.0,
            'raw_impact': dev['adjusted_technical_impact'],
            'raw_visibility': dev['adjusted_visibility_score']
        })
        
    
    # CRITICAL FIX: Sort by Overall Performance Score (which includes attendance)
    # This replaces the old sorting that ignored attendance
    processed_developers.sort(
        key=lambda x: x['overall_performance_score'], 
        reverse=True
    )
    
    # Debug: Print hidden gems count
    hidden_gems_count = len([dev for dev in processed_developers if dev.get('is_hidden_gem', False)])
    print(f"Debug: Found {hidden_gems_count} hidden gems out of {len(processed_developers)} developers")
    
    return processed_developers