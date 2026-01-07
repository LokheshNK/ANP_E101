from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from engine.scoring import DevLensKeywordScorer
import os

app = FastAPI(title="DevLens API")

# 1. Enable CORS so your Frontend can talk to the Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Define Paths to your JSON data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMM_DATA = os.path.join(BASE_DIR, "data", "comm_mock_data.json")
EXEC_DATA = os.path.join(BASE_DIR, "data", "exec_mock_data.json")

@app.get("/")
def read_root():
    return {"status": "DevLens API is Running"}

@app.get("/api/scores")
def get_quadrant_scores():
    """
    Triggers the Scorer Engine to process JSON data 
    and return X, Y coordinates for the dashboard.
    """
    try:
        # Initialize your Scorer
        scorer = DevLensKeywordScorer(COMM_DATA, EXEC_DATA)
        
        # Calculate the Z-Scores (Final Math)
        results = scorer.calculate_scores()
        
        # Get team information
        team_info = scorer.get_team_info()
        
        # Reformat for easier Frontend consumption
        formatted_data = []
        for uid, coords in results.items():
            team_data = team_info.get(uid, {})
            formatted_data.append({
                "id": uid,
                "name": team_data.get("name", f"User {uid[-3:]}"),
                "team": team_data.get("team", "Unknown"),
                "x": coords['x_final'],
                "y": coords['y_final'],
                "visibility_raw": coords.get('visibility', 0),
                "impact_raw": coords.get('impact', 0)
            })
        
        return {
            "count": len(formatted_data),
            "data": formatted_data
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/detailed-stats")
def get_detailed_execution_stats():
    """
    Returns detailed execution statistics for each team member
    """
    try:
        scorer = DevLensKeywordScorer(COMM_DATA, EXEC_DATA)
        
        # Calculate scores (this populates detailed_stats)
        results = scorer.calculate_scores()
        
        # Get detailed statistics
        detailed_stats = scorer.get_detailed_stats()
        team_info = scorer.get_team_info()
        
        # Format for frontend
        formatted_stats = []
        for uid, stats in detailed_stats.items():
            team_data = team_info.get(uid, {})
            formatted_stats.append({
                "id": uid,
                "name": team_data.get("name", f"User {uid[-3:]}"),
                "team": team_data.get("team", "Unknown"),
                "execution_stats": {
                    "total_commits": stats["total_commits"],
                    "total_additions": stats["total_additions"],
                    "total_deletions": stats["total_deletions"],
                    "total_lines_changed": stats["total_additions"] + stats["total_deletions"],
                    "total_files_changed": stats["total_files_changed"],
                    "unique_files_count": stats["unique_files_count"],
                    "total_entropy": stats["total_entropy"],
                    "avg_entropy_per_commit": stats["avg_entropy_per_commit"],
                    "avg_lines_per_commit": (
                        (stats["total_additions"] + stats["total_deletions"]) / stats["total_commits"]
                        if stats["total_commits"] > 0 else 0
                    ),
                    "avg_files_per_commit": (
                        stats["total_files_changed"] / stats["total_commits"]
                        if stats["total_commits"] > 0 else 0
                    )
                }
            })
        
        # Sort by total impact (entropy)
        formatted_stats.sort(key=lambda x: x["execution_stats"]["total_entropy"], reverse=True)
        
        return {
            "count": len(formatted_stats),
            "data": formatted_stats
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/team-analysis")
def get_team_analysis():
    """
    Returns team-based analytics and statistics
    """
    try:
        scorer = DevLensKeywordScorer(COMM_DATA, EXEC_DATA)
        results = scorer.calculate_scores()
        team_info = scorer.get_team_info()
        
        # Group by teams
        teams = {}
        for uid, coords in results.items():
            team_data = team_info.get(uid, {})
            team_name = team_data.get("team", "Unknown")
            
            if team_name not in teams:
                teams[team_name] = {
                    "name": team_name,
                    "members": [],
                    "avg_visibility": 0,
                    "avg_impact": 0,
                    "total_members": 0
                }
            
            teams[team_name]["members"].append({
                "id": uid,
                "name": team_data.get("name", f"User {uid[-3:]}"),
                "visibility": coords['x_final'],
                "impact": coords['y_final']
            })
        
        # Calculate team averages
        for team_name, team_data in teams.items():
            if team_data["members"]:
                team_data["total_members"] = len(team_data["members"])
                team_data["avg_visibility"] = sum(m["visibility"] for m in team_data["members"]) / len(team_data["members"])
                team_data["avg_impact"] = sum(m["impact"] for m in team_data["members"]) / len(team_data["members"])
        
        return {
            "teams": list(teams.values())
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)