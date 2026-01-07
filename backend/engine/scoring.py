import json
import pandas as pd
import numpy as np
from engine.nlp_filter import TechFilter # Import your filter

class DevLensKeywordScorer:
    def __init__(self, comm_path, exec_path):
        self.comm_path = comm_path
        self.exec_path = exec_path
        self.filter = TechFilter() # Initialize the filter
        
        # Define our Keyword Weights
        self.tech_weights = {
            "auth": 2.0, "bug": 1.5, "refactor": 2.5, "db": 2.0,
            "pr": 1.5, "api": 1.8, "fix": 1.2, "logic": 2.0,
            "ci": 1.5, "cd": 1.5, "test": 1.0, "deploy": 2.0
        }

    def get_visibility_weight(self, raw_content):
        clean_text = self.filter.clean_text(raw_content)
        
        weight = 1.0  
        for word, bonus in self.tech_weights.items():
            if word in clean_text:
                weight += bonus
        
        if "http" in raw_content or "github" in raw_content:
            weight += 1.5
            
        return weight

    def calculate_sophisticated_impact(self, stats):
        """
        Calculate sophisticated impact score that prevents gaming through volume
        
        Combines multiple factors:
        1. Average Entropy per Commit (quality over quantity)
        2. Log-scaled Commit Volume (diminishing returns for high volume)
        3. Unique Files Diversity (architectural breadth)
        4. Commit Size Consistency (penalizes micro-commits)
        """
        if stats['total_commits'] == 0:
            return 0.0
        
        # 1. Average Entropy per Commit (0-3+ range typically)
        # This is the primary quality metric - high entropy = complex, distributed changes
        avg_entropy = stats['avg_entropy_per_commit']
        
        # 2. Log-scaled Commit Volume (diminishing returns)
        # log(1 + commits) prevents linear scaling with commit count
        # Someone with 1000 commits doesn't get 100x the score of someone with 10
        log_commit_volume = np.log1p(stats['total_commits'])
        
        # 3. Unique Files Diversity Score
        # Rewards touching many different files (architectural impact)
        unique_files_score = np.log1p(stats['unique_files_count'])
        
        # 4. Commit Size Consistency Penalty
        # Penalize developers who make many tiny commits vs fewer substantial ones
        commit_sizes = stats['commit_sizes']
        if len(commit_sizes) > 1:
            avg_commit_size = np.mean(commit_sizes)
            commit_size_std = np.std(commit_sizes)
            
            # Coefficient of variation (std/mean) - lower is more consistent
            # High CV means mix of tiny and large commits (potentially gaming)
            cv = commit_size_std / avg_commit_size if avg_commit_size > 0 else 0
            
            # Consistency bonus: reward consistent commit sizes
            # CV of 0.5 = moderate variation, CV of 2.0+ = high variation (penalty)
            consistency_factor = max(0.5, 1.0 - (cv - 0.5) * 0.3)
        else:
            consistency_factor = 1.0
        
        # 5. Minimum Commit Size Filter
        # Heavily penalize if average commit size is too small (micro-commits)
        avg_lines_per_commit = (stats['total_additions'] + stats['total_deletions']) / stats['total_commits']
        
        if avg_lines_per_commit < 5:  # Micro-commits
            size_penalty = 0.3
        elif avg_lines_per_commit < 20:  # Small commits
            size_penalty = 0.7
        else:  # Substantial commits
            size_penalty = 1.0
        
        # Combine all factors with weights
        sophisticated_impact = (
            avg_entropy * 3.0 +                    # Primary: complexity/distribution (weight: 3)
            log_commit_volume * 0.5 +              # Secondary: volume with diminishing returns (weight: 0.5)
            unique_files_score * 1.0               # Secondary: architectural breadth (weight: 1)
        ) * consistency_factor * size_penalty      # Apply penalties
        
        return sophisticated_impact

    def _calculate_commit_consistency(self, stats):
        """Calculate commit consistency metric"""
        if len(stats['commit_sizes']) <= 1:
            return 1.0
        
        avg_size = np.mean(stats['commit_sizes'])
        std_size = np.std(stats['commit_sizes'])
        cv = std_size / avg_size if avg_size > 0 else 0
        
        # Return consistency score (higher = more consistent)
        return max(0.0, 1.0 - cv)

    def get_team_info(self):
        """Extract team information from communication data"""
        team_info = {}
        
        try:
            with open(self.comm_path, 'r', encoding='utf-8') as f:
                comm_data = json.load(f)
            
            for msg in comm_data:
                user = msg['from']['user']
                uid = user['id']
                if uid not in team_info:
                    team_info[uid] = {
                        'name': user.get('displayName', f"User {uid[-3:]}"),
                        'team': user.get('team', 'Unknown')
                    }
        except Exception as e:
            print(f"Error extracting team info: {e}")
        
        return team_info

    def calculate_scores(self):
        # --- COMMUNICATION ---
        with open(self.comm_path, 'r', encoding='utf-8') as f:
            comm_data = json.load(f)
        
        vis_map = {}
        for msg in comm_data:
            uid = msg['from']['user']['id']
            # Pass raw body to our new visibility logic
            weight = self.get_visibility_weight(msg['body']['content'])
            vis_map[uid] = vis_map.get(uid, 0) + weight

        # ---EXECUTION ---
        with open(self.exec_path, 'r', encoding='utf-8') as f:
            exec_data = json.load(f)
            
        # Comprehensive impact tracking per person
        imp_map = {}
        detailed_stats = {}
        
        for commit in exec_data:
            meta = commit['devlens_meta']
            uid = meta['teams_user_id']
            
            # Initialize person's stats if not exists
            if uid not in detailed_stats:
                detailed_stats[uid] = {
                    'total_commits': 0,
                    'total_additions': 0,
                    'total_deletions': 0,
                    'total_files_changed': 0,
                    'unique_files': set(),
                    'total_entropy': 0.0,
                    'entropy_values': [],
                    'commit_sizes': []
                }
            
            # Aggregate statistics
            stats = meta['stats']
            commit_size = stats['additions'] + stats['deletions']
            
            detailed_stats[uid]['total_commits'] += 1
            detailed_stats[uid]['total_additions'] += stats['additions']
            detailed_stats[uid]['total_deletions'] += stats['deletions']
            detailed_stats[uid]['total_files_changed'] += meta.get('files_changed', 1)
            detailed_stats[uid]['total_entropy'] += stats['total_entropy']
            detailed_stats[uid]['entropy_values'].append(stats['total_entropy'])
            detailed_stats[uid]['commit_sizes'].append(commit_size)
            
            # Track unique files (if file distribution exists)
            if 'file_distribution' in meta:
                for file_path in meta['file_distribution'].keys():
                    detailed_stats[uid]['unique_files'].add(file_path)

        # Calculate sophisticated impact scores
        for uid in detailed_stats:
            stats = detailed_stats[uid]
            
            # Convert unique files set to count
            stats['unique_files_count'] = len(stats['unique_files'])
            del stats['unique_files']  # Remove set for JSON serialization
            
            # Basic averages
            stats['avg_entropy_per_commit'] = (
                stats['total_entropy'] / stats['total_commits']
                if stats['total_commits'] > 0 else 0
            )
            
            # Calculate sophisticated impact metrics
            impact_score = self.calculate_sophisticated_impact(stats)
            imp_map[uid] = impact_score
            
            # Store the calculated impact score
            stats['sophisticated_impact'] = impact_score

        # Store detailed stats for API access
        self.detailed_stats = detailed_stats

        # --- FINAL MATH ---
        df = pd.DataFrame({'visibility': vis_map, 'impact': imp_map}).fillna(0)
        
        # Ensure we have some variance in the data
        if df['visibility'].std() == 0:
            df['visibility'] = df['visibility'] + np.random.normal(0, 0.1, len(df))
        if df['impact'].std() == 0:
            df['impact'] = df['impact'] + np.random.normal(0, 0.1, len(df))
        
        df['x_log'] = np.log1p(df['visibility'])
        df['y_log'] = np.log1p(df['impact'])
        
        # Add small epsilon to prevent division by zero
        x_std = df['x_log'].std() if df['x_log'].std() > 0 else 1.0
        y_std = df['y_log'].std() if df['y_log'].std() > 0 else 1.0
        
        df['x_final'] = (df['x_log'] - df['x_log'].mean()) / x_std
        df['y_final'] = (df['y_log'] - df['y_log'].mean()) / y_std
        
        # Store raw values for reference
        result_dict = {}
        for idx in df.index:
            result_dict[idx] = {
                'x_final': df.loc[idx, 'x_final'],
                'y_final': df.loc[idx, 'y_final'],
                'visibility': df.loc[idx, 'visibility'],
                'impact': df.loc[idx, 'impact']
            }
        
        return result_dict

    def get_detailed_stats(self):
        """Return detailed execution statistics per person"""
        return getattr(self, 'detailed_stats', {})