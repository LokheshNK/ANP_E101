import re

class TechFilter:
    def __init__(self):
        self.tech_weights = {
            "auth": 2.0, "bug": 1.5, "refactor": 2.5, "db": 2.0,
            "pr": 1.5, "api": 1.8, "fix": 1.2, "logic": 2.0,
            "ci": 1.5, "cd": 1.5, "test": 1.0, "deploy": 2.0
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