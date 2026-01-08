#!/usr/bin/env python3
"""
Test script to verify Hidden Gems are properly identified
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import DevLensDB
from engine.scoring import process_metrics
from engine.nlp_filter import analyze_communication

def test_hidden_gems():
    """Test Hidden Gems identification"""
    
    print("🔍 Testing Hidden Gems Identification")
    print("=" * 60)
    
    # Get developers for the first available company
    db = DevLensDB()
    companies = db.get_companies()
    
    if not companies:
        print("❌ No companies found!")
        return
    
    # Use the company with the most developers
    company_data = [(name, len(db.get_company_developers(name))) for _, name in companies]
    company_name = max(company_data, key=lambda x: x[1])[0]
    
    developers = db.get_company_developers(company_name)
    
    print(f"Using company: {company_name}")
    print(f"Loaded {len(developers)} developers")
    
    # Process communication scores
    for dev in developers:
        dev['comm_score'] = analyze_communication(dev['msgs'])
    
    # Add attendance data (simulate what main.py does)
    try:
        with open('data/activity_based_metrics.json', 'r') as f:
            attendance_list = json.load(f)
            attendance_data = {att['name']: att for att in attendance_list}
            
        for dev in developers:
            if dev['name'] in attendance_data:
                att_info = attendance_data[dev['name']]
                dev['attendance_rate'] = att_info['attendance_metrics']['attendance_rate']
            else:
                dev['attendance_rate'] = 0.85
                
        print("✅ Attendance data loaded successfully")
    except Exception as e:
        print(f"⚠️  Using default attendance: {e}")
        for dev in developers:
            dev['attendance_rate'] = 0.85
    
    # Process metrics
    print("\nProcessing metrics...")
    processed = process_metrics(developers)
    
    print(f"\nProcessed {len(processed)} developers")
    
    # Analyze quadrants
    quadrant_counts = {}
    for dev in processed:
        q = dev.get('quadrant', 0)
        quadrant_counts[q] = quadrant_counts.get(q, 0) + 1
    
    print(f"\nQuadrant Distribution:")
    for q in [1, 2, 3, 4]:
        count = quadrant_counts.get(q, 0)
        name = {1: "Stars", 2: "Hidden Gems", 3: "Connectors", 4: "Developing"}[q]
        print(f"  Quadrant {q} ({name}): {count} developers")
    
    # Find Hidden Gems
    hidden_gems = [dev for dev in processed if dev.get('is_hidden_gem', False)]
    quadrant_2_devs = [dev for dev in processed if dev.get('quadrant') == 2]
    
    print(f"\nHidden Gems Analysis:")
    print(f"  Developers with is_hidden_gem=True: {len(hidden_gems)}")
    print(f"  Developers in Quadrant 2: {len(quadrant_2_devs)}")
    
    if hidden_gems:
        print(f"\n✅ Found {len(hidden_gems)} Hidden Gems:")
        for gem in hidden_gems:
            impact = gem.get('raw_impact', 0)
            visibility = gem.get('raw_visibility', 0)
            attendance = gem.get('attendance_rate', 0)
            print(f"  - {gem['name']}: Impact={impact:.2f}, Visibility={visibility:.2f}, Attendance={attendance:.1%}")
    else:
        print(f"\n❌ No Hidden Gems found!")
        
        if quadrant_2_devs:
            print(f"But found {len(quadrant_2_devs)} developers in Quadrant 2:")
            for dev in quadrant_2_devs:
                impact = dev.get('raw_impact', 0)
                visibility = dev.get('raw_visibility', 0)
                attendance = dev.get('attendance_rate', 0)
                print(f"  - {dev['name']}: Impact={impact:.2f}, Visibility={visibility:.2f}, Attendance={attendance:.1%}")
    
    # Show top performers by impact
    print(f"\nTop 5 by Impact Score:")
    top_impact = sorted(processed, key=lambda x: x.get('raw_impact', 0), reverse=True)[:5]
    for i, dev in enumerate(top_impact, 1):
        impact = dev.get('raw_impact', 0)
        visibility = dev.get('raw_visibility', 0)
        quadrant = dev.get('quadrant', 0)
        is_gem = dev.get('is_hidden_gem', False)
        print(f"  {i}. {dev['name']}: Impact={impact:.2f}, Visibility={visibility:.2f}, Q{quadrant}, Gem={is_gem}")

if __name__ == "__main__":
    test_hidden_gems()