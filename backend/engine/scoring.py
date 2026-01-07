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
            
        imp_map = {}
        for commit in exec_data:
            meta = commit['devlens_meta']
            uid = meta['teams_user_id']
            entropy = meta['stats']['total_entropy']
            imp_map[uid] = imp_map.get(uid, 0) + entropy

        # --- FINAL MATH ---
        df = pd.DataFrame({'visibility': vis_map, 'impact': imp_map}).fillna(0)
        
        df['x_log'] = np.log1p(df['visibility'])
        df['y_log'] = np.log1p(df['impact'])
        
        df['x_final'] = (df['x_log'] - df['x_log'].mean()) / (df['x_log'].std() + 1e-9)
        df['y_final'] = (df['y_log'] - df['y_log'].mean()) / (df['y_log'].std() + 1e-9)
        
        return df[['x_final', 'y_final']].to_dict(orient='index')