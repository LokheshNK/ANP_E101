#!/usr/bin/env python3
"""
Real-world GitHub integration example for DevLens
This shows how to collect actual collaboration metrics from GitHub API
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class GitHubIntegration:
    def __init__(self, github_token: str, organization: str):
        self.token = github_token
        self.org = organization
        self.base_url = "https://api.github.com"
        self.headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def get_user_collaboration_metrics(self, username: str, start_date: str, end_date: str) -> Dict:
        """
        Get comprehensive collaboration metrics for a user from GitHub
        """
        metrics = {
            'code_reviews_given': 0,
            'code_reviews_received': 0,
            'pull_requests_created': 0,
            'issues_created': 0,
            'issues_commented': 0,
            'avg_review_response_time_hours': 0,
            'cross_repo_contributions': 0,
            'mentoring_activities': 0
        }
        
        try:
            # 1. Code Reviews Given
            metrics['code_reviews_given'] = self._get_reviews_given(username, start_date, end_date)
            
            # 2. Pull Requests and Reviews Received
            pr_data = self._get_pull_requests(username, start_date, end_date)
            metrics['pull_requests_created'] = len(pr_data)
            metrics['code_reviews_received'] = sum(pr.get('review_count', 0) for pr in pr_data)
            
            # 3. Issue Activity
            metrics['issues_created'] = self._get_issues_created(username, start_date, end_date)
            metrics['issues_commented'] = self._get_issue_comments(username, start_date, end_date)
            
            # 4. Response Time Analysis
            metrics['avg_review_response_time_hours'] = self._calculate_avg_response_time(username, start_date, end_date)
            
            # 5. Cross-repository Contributions
            metrics['cross_repo_contributions'] = self._get_cross_repo_activity(username, start_date, end_date)
            
            # 6. Mentoring Activities (based on PR descriptions and comments)
            metrics['mentoring_activities'] = self._detect_mentoring_activity(username, start_date, end_date)
            
        except Exception as e:
            print(f"Error collecting GitHub metrics for {username}: {e}")
        
        return metrics
    
    def _get_reviews_given(self, username: str, start_date: str, end_date: str) -> int:
        """Count code reviews given by user"""
        query = f'type:pr reviewed-by:{username} org:{self.org} created:{start_date}..{end_date}'
        
        response = requests.get(
            f'{self.base_url}/search/issues',
            headers=self.headers,
            params={'q': query, 'per_page': 100}
        )
        
        if response.status_code == 200:
            return response.json().get('total_count', 0)
        return 0
    
    def _get_pull_requests(self, username: str, start_date: str, end_date: str) -> List[Dict]:
        """Get pull requests created by user with review information"""
        query = f'type:pr author:{username} org:{self.org} created:{start_date}..{end_date}'
        
        response = requests.get(
            f'{self.base_url}/search/issues',
            headers=self.headers,
            params={'q': query, 'per_page': 100}
        )
        
        if response.status_code != 200:
            return []
        
        prs = response.json().get('items', [])
        
        # Enrich with review count for each PR
        for pr in prs:
            pr_number = pr['number']
            repo_name = pr['repository_url'].split('/')[-1]
            
            # Get reviews for this PR
            reviews_response = requests.get(
                f'{self.base_url}/repos/{self.org}/{repo_name}/pulls/{pr_number}/reviews',
                headers=self.headers
            )
            
            if reviews_response.status_code == 200:
                pr['review_count'] = len(reviews_response.json())
            else:
                pr['review_count'] = 0
        
        return prs
    
    def _get_issues_created(self, username: str, start_date: str, end_date: str) -> int:
        """Count issues created by user"""
        query = f'type:issue author:{username} org:{self.org} created:{start_date}..{end_date}'
        
        response = requests.get(
            f'{self.base_url}/search/issues',
            headers=self.headers,
            params={'q': query, 'per_page': 100}
        )
        
        if response.status_code == 200:
            return response.json().get('total_count', 0)
        return 0
    
    def _get_issue_comments(self, username: str, start_date: str, end_date: str) -> int:
        """Count issue comments by user"""
        query = f'type:issue commenter:{username} org:{self.org} updated:{start_date}..{end_date}'
        
        response = requests.get(
            f'{self.base_url}/search/issues',
            headers=self.headers,
            params={'q': query, 'per_page': 100}
        )
        
        if response.status_code == 200:
            return response.json().get('total_count', 0)
        return 0
    
    def _calculate_avg_response_time(self, username: str, start_date: str, end_date: str) -> float:
        """Calculate average response time to review requests"""
        # This is a simplified version - in practice, you'd need to:
        # 1. Get all PRs where user was requested as reviewer
        # 2. Find the time between request and first review
        # 3. Calculate average
        
        # For demo purposes, return a mock calculation
        # In real implementation, this would involve more complex API calls
        return 24.5  # hours
    
    def _get_cross_repo_activity(self, username: str, start_date: str, end_date: str) -> int:
        """Count contributions across different repositories"""
        # Get all repositories user contributed to
        response = requests.get(
            f'{self.base_url}/search/commits',
            headers=self.headers,
            params={
                'q': f'author:{username} org:{self.org} author-date:{start_date}..{end_date}',
                'per_page': 100
            }
        )
        
        if response.status_code != 200:
            return 0
        
        commits = response.json().get('items', [])
        unique_repos = set()
        
        for commit in commits:
            repo_name = commit['repository']['name']
            unique_repos.add(repo_name)
        
        return len(unique_repos)
    
    def _detect_mentoring_activity(self, username: str, start_date: str, end_date: str) -> int:
        """Detect mentoring activities based on PR/issue interactions"""
        mentoring_keywords = [
            'explained', 'helped', 'guided', 'taught', 'mentored',
            'walkthrough', 'pair programming', 'code review feedback',
            'learning', 'tutorial', 'best practice'
        ]
        
        # Search for comments containing mentoring keywords
        mentoring_count = 0
        
        for keyword in mentoring_keywords:
            query = f'type:pr commenter:{username} org:{self.org} "{keyword}" updated:{start_date}..{end_date}'
            
            response = requests.get(
                f'{self.base_url}/search/issues',
                headers=self.headers,
                params={'q': query, 'per_page': 10}
            )
            
            if response.status_code == 200:
                mentoring_count += response.json().get('total_count', 0)
        
        return min(mentoring_count, 50)  # Cap to avoid over-counting
    
    def get_innovation_metrics(self, username: str, start_date: str, end_date: str) -> Dict:
        """Get innovation-related metrics"""
        metrics = {
            'feature_proposals': 0,
            'bug_reports': 0,
            'documentation_improvements': 0,
            'process_improvements': 0
        }
        
        # Feature proposals (issues with enhancement label)
        query = f'type:issue author:{username} org:{self.org} label:enhancement created:{start_date}..{end_date}'
        response = requests.get(
            f'{self.base_url}/search/issues',
            headers=self.headers,
            params={'q': query}
        )
        if response.status_code == 200:
            metrics['feature_proposals'] = response.json().get('total_count', 0)
        
        # Bug reports
        query = f'type:issue author:{username} org:{self.org} label:bug created:{start_date}..{end_date}'
        response = requests.get(
            f'{self.base_url}/search/issues',
            headers=self.headers,
            params={'q': query}
        )
        if response.status_code == 200:
            metrics['bug_reports'] = response.json().get('total_count', 0)
        
        # Documentation improvements (PRs affecting .md files)
        query = f'type:pr author:{username} org:{self.org} filename:*.md created:{start_date}..{end_date}'
        response = requests.get(
            f'{self.base_url}/search/issues',
            headers=self.headers,
            params={'q': query}
        )
        if response.status_code == 200:
            metrics['documentation_improvements'] = response.json().get('total_count', 0)
        
        return metrics

# Example usage
if __name__ == "__main__":
    # This would be used in production like this:
    
    github_integration = GitHubIntegration(
        github_token="your_github_token_here",
        organization="your_org_name"
    )
    
    # Get metrics for a user
    start_date = "2024-01-01"
    end_date = "2024-03-31"
    username = "john_doe"
    
    collaboration_metrics = github_integration.get_user_collaboration_metrics(
        username, start_date, end_date
    )
    
    innovation_metrics = github_integration.get_innovation_metrics(
        username, start_date, end_date
    )
    
    print("Collaboration Metrics:")
    print(json.dumps(collaboration_metrics, indent=2))
    
    print("\nInnovation Metrics:")
    print(json.dumps(innovation_metrics, indent=2))