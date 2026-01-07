#!/usr/bin/env python3

import math
import json

def calculate_shannon_entropy(file_changes):
    """
    Calculate Shannon entropy based on distribution of effort across files
    H(X) = -Σ(Pi * log2(Pi))
    where Pi = (additions + deletions for file i) / total changes
    """
    if not file_changes:
        return 0.0
    
    # Calculate total changes across all files
    total_changes = sum(changes for changes in file_changes.values())
    
    if total_changes == 0:
        return 0.0
    
    # Calculate entropy
    entropy = 0.0
    for file_path, changes in file_changes.items():
        if changes > 0:
            pi = changes / total_changes
            entropy -= pi * math.log2(pi)
    
    return entropy

def test_entropy_examples():
    print("Shannon Entropy Test Cases:")
    print("=" * 50)
    
    # Test case 1: Single file (minimum entropy)
    single_file = {"file1.py": 100}
    entropy1 = calculate_shannon_entropy(single_file)
    print(f"1 file, all changes: {entropy1:.4f} (should be 0.0)")
    
    # Test case 2: Two files, equal distribution (maximum entropy for 2 files)
    equal_two = {"file1.py": 50, "file2.py": 50}
    entropy2 = calculate_shannon_entropy(equal_two)
    print(f"2 files, equal split: {entropy2:.4f} (should be 1.0)")
    
    # Test case 3: Two files, unequal distribution
    unequal_two = {"file1.py": 80, "file2.py": 20}
    entropy3 = calculate_shannon_entropy(unequal_two)
    print(f"2 files, 80/20 split: {entropy3:.4f}")
    
    # Test case 4: Three files, equal distribution
    equal_three = {"file1.py": 33, "file2.py": 33, "file3.py": 34}
    entropy4 = calculate_shannon_entropy(equal_three)
    print(f"3 files, equal split: {entropy4:.4f} (should be ~1.585)")
    
    # Test case 5: Many files, equal distribution
    equal_four = {"file1.py": 25, "file2.py": 25, "file3.py": 25, "file4.py": 25}
    entropy5 = calculate_shannon_entropy(equal_four)
    print(f"4 files, equal split: {entropy5:.4f} (should be 2.0)")
    
    print("\nInterpretation:")
    print("- Higher entropy = more distributed effort across files")
    print("- Lower entropy = effort concentrated in fewer files")
    print("- Range: 0 (single file) to log2(n) where n = number of files")

def analyze_sample_commits():
    print("\n" + "=" * 50)
    print("Sample Commit Analysis:")
    print("=" * 50)
    
    try:
        with open("data/exec_mock_data.json", "r") as f:
            commits = json.load(f)
        
        # Analyze first 10 commits
        for i, commit in enumerate(commits[:10]):
            meta = commit["devlens_meta"]
            file_dist = meta["file_distribution"]
            entropy = meta["stats"]["total_entropy"]
            
            print(f"\nCommit {i+1} by {commit['commit']['author']['name']} ({meta['team']}):")
            print(f"  Files changed: {meta['files_changed']}")
            print(f"  File distribution: {file_dist}")
            print(f"  Shannon entropy: {entropy:.4f}")
            
            # Verify our calculation matches
            calculated_entropy = calculate_shannon_entropy(file_dist)
            print(f"  Verified entropy: {calculated_entropy:.4f}")
            
    except FileNotFoundError:
        print("exec_mock_data.json not found. Run generate_exec_data.py first.")

if __name__ == "__main__":
    test_entropy_examples()
    analyze_sample_commits()