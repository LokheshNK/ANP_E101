#!/usr/bin/env python3
"""
Demo script showing the different employee profiles across companies
"""

from database import DevLensDB

def show_company_profiles():
    db = DevLensDB()
    
    companies = ["TechCorp Inc.", "Innovate Solutions", "StartupIO"]
    
    for company in companies:
        print(f"\n{'='*60}")
        print(f"🏢 {company}")
        print(f"{'='*60}")
        
        developers = db.get_company_developers(company)
        
        if not developers:
            print("No developers found for this company.")
            continue
        
        # Calculate company averages
        total_commits = sum(dev['commits'] for dev in developers)
        avg_commits = total_commits / len(developers)
        avg_entropy = sum(dev['entropy'] for dev in developers) / len(developers)
        avg_meetings = sum(dev['meetings'] for dev in developers) / len(developers)
        
        print(f"📊 Company Overview:")
        print(f"   • Total Developers: {len(developers)}")
        print(f"   • Average Commits: {avg_commits:.1f}")
        print(f"   • Average Complexity: {avg_entropy:.2f}")
        print(f"   • Average Meetings: {avg_meetings:.1f}")
        
        # Group by teams
        teams = {}
        for dev in developers:
            team = dev['team']
            if team not in teams:
                teams[team] = []
            teams[team].append(dev)
        
        print(f"\n👥 Teams ({len(teams)} teams):")
        for team_name, team_devs in teams.items():
            team_commits = sum(dev['commits'] for dev in team_devs)
            team_avg_entropy = sum(dev['entropy'] for dev in team_devs) / len(team_devs)
            print(f"   • {team_name}: {len(team_devs)} developers, {team_commits} total commits, {team_avg_entropy:.2f} avg complexity")
        
        # Show top performers
        top_performers = sorted(developers, key=lambda x: x['commits'], reverse=True)[:3]
        print(f"\n🏆 Top Performers (by commits):")
        for i, dev in enumerate(top_performers, 1):
            print(f"   {i}. {dev['name']} ({dev['team']}) - {dev['commits']} commits, {dev['entropy']:.2f} complexity")
        
        # Show communication leaders
        comm_leaders = sorted(developers, key=lambda x: x['meetings'], reverse=True)[:3]
        print(f"\n💬 Communication Leaders (by meetings):")
        for i, dev in enumerate(comm_leaders, 1):
            print(f"   {i}. {dev['name']} ({dev['team']}) - {dev['meetings']} meetings/week")
        
        # Show complexity leaders
        complexity_leaders = sorted(developers, key=lambda x: x['entropy'], reverse=True)[:3]
        print(f"\n🧠 Technical Complexity Leaders:")
        for i, dev in enumerate(complexity_leaders, 1):
            print(f"   {i}. {dev['name']} ({dev['team']}) - {dev['entropy']:.2f} complexity score")

def show_company_culture_analysis():
    db = DevLensDB()
    
    print(f"\n{'='*80}")
    print(f"🎯 COMPANY CULTURE ANALYSIS")
    print(f"{'='*80}")
    
    companies = ["TechCorp Inc.", "Innovate Solutions", "StartupIO"]
    
    for company in companies:
        developers = db.get_company_developers(company)
        if not developers:
            continue
            
        avg_commits = sum(dev['commits'] for dev in developers) / len(developers)
        avg_entropy = sum(dev['entropy'] for dev in developers) / len(developers)
        avg_meetings = sum(dev['meetings'] for dev in developers) / len(developers)
        
        print(f"\n🏢 {company}")
        print(f"   Commits/Developer: {avg_commits:.1f}")
        print(f"   Technical Complexity: {avg_entropy:.2f}")
        print(f"   Meeting Load: {avg_meetings:.1f}")
        
        # Determine culture type
        if avg_meetings > 10:
            culture = "🗣️  High Communication Culture"
        elif avg_entropy > 0.8:
            culture = "🔬 Technical Excellence Culture"
        elif avg_commits > 20:
            culture = "⚡ High Velocity Culture"
        else:
            culture = "⚖️  Balanced Culture"
        
        print(f"   Culture Type: {culture}")
        
        # Performance distribution
        high_performers = len([d for d in developers if d['commits'] > avg_commits * 1.2])
        low_performers = len([d for d in developers if d['commits'] < avg_commits * 0.8])
        
        print(f"   Performance Distribution:")
        print(f"     • High Performers: {high_performers}/{len(developers)} ({high_performers/len(developers)*100:.0f}%)")
        print(f"     • Average Performers: {len(developers) - high_performers - low_performers}/{len(developers)}")
        print(f"     • Developing Talent: {low_performers}/{len(developers)} ({low_performers/len(developers)*100:.0f}%)")

if __name__ == "__main__":
    print("🚀 DevLens Company Profiles Demo")
    show_company_profiles()
    show_company_culture_analysis()
    
    print(f"\n{'='*80}")
    print("💡 Key Insights:")
    print("• TechCorp Inc.: Traditional enterprise with process-heavy culture")
    print("• Innovate Solutions: Modern agile startup with high collaboration")  
    print("• StartupIO: Lean tech startup focused on high performance")
    print(f"{'='*80}")