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
                    'entropy_values': []
                }
            
            # Aggregate statistics
            stats = meta['stats']
            detailed_stats[uid]['total_commits'] += 1
            detailed_stats[uid]['total_additions'] += stats['additions']
            detailed_stats[uid]['total_deletions'] += stats['deletions']
            detailed_stats[uid]['total_files_changed'] += meta.get('files_changed', 1)
            detailed_stats[uid]['total_entropy'] += stats['total_entropy']
            detailed_stats[uid]['entropy_values'].append(stats['total_entropy'])
            
            # Track unique files (if file distribution exists)
            if 'file_distribution' in meta:
                for file_path in meta['file_distribution'].keys():
                    detailed_stats[uid]['unique_files'].add(file_path)
            
            # Use entropy as the main impact score (as before)
            imp_map[uid] = imp_map.get(uid, 0) + stats['total_entropy']

        # Convert unique files set to count
        for uid in detailed_stats:
            detailed_stats[uid]['unique_files_count'] = len(detailed_stats[uid]['unique_files'])
            detailed_stats[uid]['avg_entropy_per_commit'] = (
                detailed_stats[uid]['total_entropy'] / detailed_stats[uid]['total_commits']
                if detailed_stats[uid]['total_commits'] > 0 else 0
            )
            # Remove the set object for JSON serialization
            del detailed_stats[uid]['unique_files']

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