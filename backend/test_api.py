#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine.scoring import DevLensKeywordScorer

def test_scoring():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    COMM_DATA = os.path.join(BASE_DIR, "data", "comm_mock_data.json")
    EXEC_DATA = os.path.join(BASE_DIR, "data", "exec_mock_data.json")
    
    print(f"Testing with files:")
    print(f"  Comm: {COMM_DATA}")
    print(f"  Exec: {EXEC_DATA}")
    
    try:
        scorer = DevLensKeywordScorer(COMM_DATA, EXEC_DATA)
        results = scorer.calculate_scores()
        team_info = scorer.get_team_info()
        
        print(f"\nResults: {len(results)} users processed")
        print(f"Team info: {len(team_info)} users with team data")
        
        # Show sample results
        sample_users = list(results.items())[:5]
        print(f"\nSample results:")
        for uid, coords in sample_users:
            team_data = team_info.get(uid, {})
            print(f"  {uid}: {team_data.get('name', 'Unknown')} ({team_data.get('team', 'No Team')})")
            print(f"    Visibility: {coords['x_final']:.3f}, Impact: {coords['y_final']:.3f}")
        
        # Check for zero averages issue
        all_x = [coords['x_final'] for coords in results.values()]
        all_y = [coords['y_final'] for coords in results.values()]
        
        avg_x = sum(all_x) / len(all_x) if all_x else 0
        avg_y = sum(all_y) / len(all_y) if all_y else 0
        
        print(f"\nOverall averages:")
        print(f"  Avg Visibility: {avg_x:.3f}")
        print(f"  Avg Impact: {avg_y:.3f}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_scoring()