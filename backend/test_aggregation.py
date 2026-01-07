#!/usr/bin/env python3

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine.scoring import DevLensKeywordScorer

def analyze_person_aggregation():
    """
    Show step-by-step how data is aggregated for each person
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    COMM_DATA = os.path.join(BASE_DIR, "data", "comm_mock_data.json")
    EXEC_DATA = os.path.join(BASE_DIR, "data", "exec_mock_data.json")
    
    print("=" * 60)
    print("PERSON AGGREGATION ANALYSIS")
    print("=" * 60)
    
    try:
        # Load raw execution data
        with open(EXEC_DATA, 'r', encoding='utf-8') as f:
            exec_data = json.load(f)
        
        # Manual aggregation to show the process
        person_stats = {}
        
        print(f"\nProcessing {len(exec_data)} commits...")
        print("\nStep-by-step aggregation for first few people:\n")
        
        for i, commit in enumerate(exec_data):
            meta = commit['devlens_meta']
            uid = meta['teams_user_id']
            author_name = commit['commit']['author']['name']
            
            # Initialize if new person
            if uid not in person_stats:
                person_stats[uid] = {
                    'name': author_name,
                    'team': meta.get('team', 'Unknown'),
                    'commits': [],
                    'total_additions': 0,
                    'total_deletions': 0,
                    'total_files_changed': 0,
                    'total_entropy': 0.0,
                    'unique_files': set()
                }
            
            # Add this commit's data
            stats = meta['stats']
            person_stats[uid]['commits'].append({
                'sha': commit['sha'][:12],
                'additions': stats['additions'],
                'deletions': stats['deletions'],
                'files_changed': meta.get('files_changed', 1),
                'entropy': stats['total_entropy']
            })
            
            # Aggregate totals
            person_stats[uid]['total_additions'] += stats['additions']
            person_stats[uid]['total_deletions'] += stats['deletions']
            person_stats[uid]['total_files_changed'] += meta.get('files_changed', 1)
            person_stats[uid]['total_entropy'] += stats['total_entropy']
            
            # Track unique files
            if 'file_distribution' in meta:
                for file_path in meta['file_distribution'].keys():
                    person_stats[uid]['unique_files'].add(file_path)
        
        # Show results for top 5 contributors
        sorted_people = sorted(person_stats.items(), 
                             key=lambda x: x[1]['total_entropy'], 
                             reverse=True)[:5]
        
        for uid, stats in sorted_people:
            print(f"👤 {stats['name']} ({stats['team']}) - ID: {uid}")
            print(f"   📊 Total Commits: {len(stats['commits'])}")
            print(f"   ➕ Total Additions: {stats['total_additions']:,}")
            print(f"   ➖ Total Deletions: {stats['total_deletions']:,}")
            print(f"   📝 Total Lines Changed: {stats['total_additions'] + stats['total_deletions']:,}")
            print(f"   📁 Total Files Touched: {stats['total_files_changed']}")
            print(f"   🎯 Unique Files: {len(stats['unique_files'])}")
            print(f"   🔢 Total Entropy: {stats['total_entropy']:.4f}")
            print(f"   📈 Avg Lines/Commit: {(stats['total_additions'] + stats['total_deletions']) / len(stats['commits']):.1f}")
            print(f"   📂 Avg Files/Commit: {stats['total_files_changed'] / len(stats['commits']):.1f}")
            
            # Show first 3 commits as examples
            print(f"   🔍 Sample Commits:")
            for commit in stats['commits'][:3]:
                print(f"      {commit['sha']}: +{commit['additions']} -{commit['deletions']} "
                      f"({commit['files_changed']} files, entropy: {commit['entropy']:.3f})")
            
            if len(stats['commits']) > 3:
                print(f"      ... and {len(stats['commits']) - 3} more commits")
            print()
        
        # Now test the scoring engine
        print("=" * 60)
        print("TESTING SCORING ENGINE")
        print("=" * 60)
        
        scorer = DevLensKeywordScorer(COMM_DATA, EXEC_DATA)
        results = scorer.calculate_scores()
        detailed_stats = scorer.get_detailed_stats()
        
        print(f"\nScoring engine processed {len(results)} people")
        print(f"Detailed stats available for {len(detailed_stats)} people")
        
        # Compare manual vs engine results
        print(f"\nVerification (Manual vs Engine):")
        for uid in list(sorted_people)[:3]:
            uid = uid[0]  # Extract UID from tuple
            manual = person_stats[uid]
            engine = detailed_stats.get(uid, {})
            
            print(f"\n{manual['name']}:")
            print(f"  Commits: Manual={len(manual['commits'])}, Engine={engine.get('total_commits', 'N/A')}")
            print(f"  Additions: Manual={manual['total_additions']}, Engine={engine.get('total_additions', 'N/A')}")
            print(f"  Deletions: Manual={manual['total_deletions']}, Engine={engine.get('total_deletions', 'N/A')}")
            print(f"  Files: Manual={manual['total_files_changed']}, Engine={engine.get('total_files_changed', 'N/A')}")
            print(f"  Entropy: Manual={manual['total_entropy']:.4f}, Engine={engine.get('total_entropy', 'N/A')}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_person_aggregation()