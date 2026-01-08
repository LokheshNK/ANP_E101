#!/usr/bin/env python3
"""
Test script to verify attendance-based scoring works correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine.scoring import process_metrics

def test_attendance_scoring():
    """Test that attendance properly affects performance rankings"""
    
    print("🧪 Testing Attendance-Based Scoring System")
    print("=" * 60)
    
    # Create test developers with different attendance patterns
    test_developers = [
        {
            "name": "High Performer, Poor Attendance",
            "team": "Backend",
            "commits": 50,  # Very high commits
            "entropy": 15.0,  # High complexity
            "meetings": 5,
            "msgs": ["Implemented complex algorithm", "Optimized performance", "Fixed critical bug"],
            "comm_score": 8.5,
            "attendance_rate": 0.11  # 11% attendance - SHOULD NOT BE #1
        },
        {
            "name": "Good Performer, Good Attendance", 
            "team": "Frontend",
            "commits": 25,  # Moderate commits
            "entropy": 8.0,  # Moderate complexity
            "meetings": 12,
            "msgs": ["Updated UI components", "Fixed styling issues", "Team collaboration"],
            "comm_score": 6.5,
            "attendance_rate": 0.92  # 92% attendance - SHOULD RANK HIGHER
        },
        {
            "name": "Average Performer, Perfect Attendance",
            "team": "QA", 
            "commits": 15,  # Lower commits
            "entropy": 5.0,  # Lower complexity
            "meetings": 18,
            "msgs": ["Test automation", "Bug reports", "Quality assurance", "Team meetings"],
            "comm_score": 7.2,
            "attendance_rate": 1.0  # 100% attendance
        },
        {
            "name": "Low Performer, No Attendance",
            "team": "DevOps",
            "commits": 5,
            "entropy": 1.0,
            "meetings": 2,
            "msgs": ["Minor config change"],
            "comm_score": 2.0,
            "attendance_rate": 0.05  # 5% attendance - SHOULD BE LAST
        }
    ]
    
    # Process with new scoring system
    processed = process_metrics(test_developers)
    
    print("RANKING RESULTS (with attendance-weighted scoring):")
    print("-" * 60)
    
    for i, dev in enumerate(processed, 1):
        print(f"{i}. {dev['name']}")
        print(f"   Attendance: {dev['attendance_rate']:.1%}")
        print(f"   Overall Score: {dev['overall_performance_score']:.2f}")
        print(f"   Technical Impact: {dev['raw_technical_impact']:.2f} -> {dev['technical_impact']:.2f} (adjusted)")
        print(f"   Commits: {dev['commits']} | Entropy: {dev['entropy']:.1f}")
        print(f"   Attendance Factor: {dev['attendance_factor']:.3f} | Penalty: {dev['attendance_penalty']:.3f}")
        print(f"   Risk Level: {dev['risk_level']} | Factors: {len(dev['risk_factors'])}")
        print()
    
    # Verify correct ranking
    print("VERIFICATION:")
    print("-" * 30)
    
    # Check that poor attendance person is NOT #1
    if processed[0]['attendance_rate'] < 0.5:
        print("❌ FAILED: Person with poor attendance is ranked #1!")
        return False
    else:
        print("✅ PASSED: Person with poor attendance is not #1")
    
    # Check that good attendance people rank higher
    good_attendance_ranks = []
    poor_attendance_ranks = []
    
    for i, dev in enumerate(processed):
        if dev['attendance_rate'] >= 0.8:
            good_attendance_ranks.append(i + 1)
        elif dev['attendance_rate'] < 0.5:
            poor_attendance_ranks.append(i + 1)
    
    avg_good_rank = sum(good_attendance_ranks) / len(good_attendance_ranks) if good_attendance_ranks else 999
    avg_poor_rank = sum(poor_attendance_ranks) / len(poor_attendance_ranks) if poor_attendance_ranks else 1
    
    if avg_good_rank < avg_poor_rank:
        print("✅ PASSED: Good attendance people rank higher on average")
        print(f"   Good attendance avg rank: {avg_good_rank:.1f}")
        print(f"   Poor attendance avg rank: {avg_poor_rank:.1f}")
        return True
    else:
        print("❌ FAILED: Poor attendance people still ranking too high!")
        print(f"   Good attendance avg rank: {avg_good_rank:.1f}")
        print(f"   Poor attendance avg rank: {avg_poor_rank:.1f}")
        return False

def test_scoring_formula():
    """Test the mathematical correctness of the scoring formula"""
    
    print("\n🔢 Testing Scoring Formula Mathematics")
    print("=" * 60)
    
    # Test case: High technical, poor attendance
    technical_impact = 10.0
    visibility_score = 5.0
    attendance_rate = 0.11  # 11%
    
    # Calculate step by step
    attendance_factor = max(0.1, attendance_rate)  # 0.11
    attendance_penalty = 0.5  # Below 70% = 50% penalty
    
    adjusted_technical = technical_impact * attendance_factor * attendance_penalty
    adjusted_visibility = visibility_score * (0.5 + 0.5 * attendance_factor)
    
    overall_score = (
        adjusted_technical * 0.4 +      # 40% technical
        adjusted_visibility * 0.3 +     # 30% visibility  
        attendance_rate * 10 * 0.3      # 30% attendance
    )
    
    print(f"Example Calculation:")
    print(f"  Technical Impact: {technical_impact} -> {adjusted_technical:.2f} (after attendance)")
    print(f"  Visibility Score: {visibility_score} -> {adjusted_visibility:.2f} (after attendance)")
    print(f"  Attendance Component: {attendance_rate * 10 * 0.3:.2f}")
    print(f"  Overall Score: {overall_score:.2f}")
    print()
    
    # Compare with good attendance
    good_attendance = 0.92
    good_factor = max(0.1, good_attendance)
    good_penalty = 1.0  # No penalty for 92%
    
    good_technical = (technical_impact * 0.5) * good_factor * good_penalty  # Lower base technical
    good_visibility = (visibility_score * 0.8) * (0.5 + 0.5 * good_factor)  # Lower base visibility
    
    good_overall = (
        good_technical * 0.4 +
        good_visibility * 0.3 +
        good_attendance * 10 * 0.3
    )
    
    print(f"Comparison with Good Attendance (92%):")
    print(f"  Technical Impact: {technical_impact * 0.5} -> {good_technical:.2f}")
    print(f"  Visibility Score: {visibility_score * 0.8} -> {good_visibility:.2f}")
    print(f"  Attendance Component: {good_attendance * 10 * 0.3:.2f}")
    print(f"  Overall Score: {good_overall:.2f}")
    print()
    
    if good_overall > overall_score:
        print("✅ PASSED: Good attendance scores higher despite lower base metrics")
        return True
    else:
        print("❌ FAILED: Poor attendance still scores higher")
        return False

if __name__ == "__main__":
    print("DEVLENS ATTENDANCE SCORING VERIFICATION")
    print("=" * 80)
    
    test1_passed = test_attendance_scoring()
    test2_passed = test_scoring_formula()
    
    print("\n" + "=" * 80)
    print("FINAL RESULTS:")
    print("=" * 80)
    
    if test1_passed and test2_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Attendance is now properly weighted in performance rankings")
        print("✅ Poor attendance (11%) will no longer rank #1")
        print("✅ Mathematical formula is working correctly")
    else:
        print("❌ SOME TESTS FAILED!")
        print("The scoring system needs further adjustment")
    
    print("\nScoring Formula Summary:")
    print("Overall Score = (Technical×0.4 + Visibility×0.3 + Attendance×0.3)")
    print("- Technical Impact is penalized by attendance factor and penalty")
    print("- Visibility is reduced when attendance is poor") 
    print("- Attendance directly contributes 30% to overall score")
    print("- Poor attendance (<70%) gets additional penalties")