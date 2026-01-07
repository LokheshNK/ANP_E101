#!/usr/bin/env python3

import numpy as np
import math

def calculate_sophisticated_impact(stats):
    """
    Test version of the sophisticated impact calculation
    """
    if stats['total_commits'] == 0:
        return 0.0
    
    # 1. Average Entropy per Commit
    avg_entropy = stats['avg_entropy_per_commit']
    
    # 2. Log-scaled Commit Volume
    log_commit_volume = np.log1p(stats['total_commits'])
    
    # 3. Unique Files Diversity Score
    unique_files_score = np.log1p(stats['unique_files_count'])
    
    # 4. Commit Size Consistency Penalty
    commit_sizes = stats['commit_sizes']
    if len(commit_sizes) > 1:
        avg_commit_size = np.mean(commit_sizes)
        commit_size_std = np.std(commit_sizes)
        cv = commit_size_std / avg_commit_size if avg_commit_size > 0 else 0
        consistency_factor = max(0.5, 1.0 - (cv - 0.5) * 0.3)
    else:
        consistency_factor = 1.0
    
    # 5. Minimum Commit Size Filter
    avg_lines_per_commit = (stats['total_additions'] + stats['total_deletions']) / stats['total_commits']
    
    if avg_lines_per_commit < 5:
        size_penalty = 0.3
    elif avg_lines_per_commit < 20:
        size_penalty = 0.7
    else:
        size_penalty = 1.0
    
    # Combine all factors
    sophisticated_impact = (
        avg_entropy * 3.0 +
        log_commit_volume * 0.5 +
        unique_files_score * 1.0
    ) * consistency_factor * size_penalty
    
    return sophisticated_impact

def test_gaming_scenarios():
    """
    Test different scenarios to show how the algorithm prevents gaming
    """
    print("=" * 80)
    print("GAMING PREVENTION TEST")
    print("=" * 80)
    
    # Scenario 1: High-volume, low-quality commits (THE GAMER)
    gamer_stats = {
        'total_commits': 1000,
        'total_additions': 2000,  # 2 lines per commit on average
        'total_deletions': 1000,   # 1 line deleted per commit
        'unique_files_count': 5,   # Only touches 5 files total
        'total_entropy': 100.0,    # Low entropy per commit (0.1 avg)
        'avg_entropy_per_commit': 0.1,  # Very low complexity
        'commit_sizes': [3] * 1000,  # Consistent tiny commits
        'entropy_values': [0.1] * 1000
    }
    
    # Scenario 2: Architectural changes (THE ARCHITECT)
    architect_stats = {
        'total_commits': 10,
        'total_additions': 2000,   # 200 lines per commit
        'total_deletions': 800,    # 80 lines deleted per commit
        'unique_files_count': 50,  # Touches many different files
        'total_entropy': 18.0,     # High entropy per commit (1.8 avg)
        'avg_entropy_per_commit': 1.8,  # High complexity/distribution
        'commit_sizes': [280] * 10,  # Substantial, consistent commits
        'entropy_values': [1.8] * 10
    }
    
    # Scenario 3: Balanced contributor (THE PROFESSIONAL)
    professional_stats = {
        'total_commits': 50,
        'total_additions': 3000,   # 60 lines per commit
        'total_deletions': 1500,   # 30 lines deleted per commit
        'unique_files_count': 25,  # Good file diversity
        'total_entropy': 60.0,     # Good entropy (1.2 avg)
        'avg_entropy_per_commit': 1.2,  # Moderate complexity
        'commit_sizes': [90] * 50,  # Reasonable commit sizes
        'entropy_values': [1.2] * 50
    }
    
    # Scenario 4: Inconsistent committer (THE CHAOTIC)
    chaotic_stats = {
        'total_commits': 100,
        'total_additions': 5000,
        'total_deletions': 2000,
        'unique_files_count': 30,
        'total_entropy': 80.0,
        'avg_entropy_per_commit': 0.8,
        'commit_sizes': [1, 2, 1, 500, 3, 1, 400, 2, 1, 300] * 10,  # Very inconsistent
        'entropy_values': [0.8] * 100
    }
    
    scenarios = [
        ("🎮 THE GAMER (1000 tiny commits)", gamer_stats),
        ("🏗️  THE ARCHITECT (10 major changes)", architect_stats),
        ("👔 THE PROFESSIONAL (50 balanced commits)", professional_stats),
        ("🌪️  THE CHAOTIC (inconsistent commits)", chaotic_stats)
    ]
    
    print("\nScenario Analysis:")
    print("-" * 80)
    
    results = []
    for name, stats in scenarios:
        # Calculate old method (simple sum)
        old_impact = stats['total_entropy']
        
        # Calculate new sophisticated method
        new_impact = calculate_sophisticated_impact(stats)
        
        # Calculate metrics for analysis
        avg_lines_per_commit = (stats['total_additions'] + stats['total_deletions']) / stats['total_commits']
        cv = np.std(stats['commit_sizes']) / np.mean(stats['commit_sizes']) if np.mean(stats['commit_sizes']) > 0 else 0
        
        results.append((name, old_impact, new_impact, stats))
        
        print(f"\n{name}")
        print(f"  📊 Commits: {stats['total_commits']}")
        print(f"  📝 Avg Lines/Commit: {avg_lines_per_commit:.1f}")
        print(f"  📁 Unique Files: {stats['unique_files_count']}")
        print(f"  🔢 Avg Entropy/Commit: {stats['avg_entropy_per_commit']:.3f}")
        print(f"  📈 Commit Size CV: {cv:.2f}")
        print(f"  🔴 Old Impact (Sum): {old_impact:.2f}")
        print(f"  🟢 New Impact (Sophisticated): {new_impact:.2f}")
        print(f"  📊 Impact Ratio (New/Old): {new_impact/old_impact:.3f}")
    
    print("\n" + "=" * 80)
    print("RANKING COMPARISON")
    print("=" * 80)
    
    # Sort by old method
    old_ranking = sorted(results, key=lambda x: x[1], reverse=True)
    print("\n🔴 OLD METHOD RANKING (Simple Sum):")
    for i, (name, old_impact, new_impact, stats) in enumerate(old_ranking, 1):
        print(f"  {i}. {name}: {old_impact:.2f}")
    
    # Sort by new method
    new_ranking = sorted(results, key=lambda x: x[2], reverse=True)
    print("\n🟢 NEW METHOD RANKING (Sophisticated):")
    for i, (name, old_impact, new_impact, stats) in enumerate(new_ranking, 1):
        print(f"  {i}. {name}: {new_impact:.2f}")
    
    print("\n" + "=" * 80)
    print("KEY INSIGHTS")
    print("=" * 80)
    print("✅ The Architect now ranks higher despite fewer commits")
    print("✅ The Gamer is penalized for micro-commits and low complexity")
    print("✅ The Professional maintains good standing with balanced approach")
    print("✅ The Chaotic is penalized for inconsistent commit patterns")
    print("\n🎯 The new algorithm rewards QUALITY over QUANTITY!")

if __name__ == "__main__":
    test_gaming_scenarios()