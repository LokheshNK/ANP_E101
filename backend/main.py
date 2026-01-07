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
        
        # Reformat for easier Frontend consumption
        # [{ "id": "teams_001", "x": 1.2, "y": -0.5 }, ...]
        formatted_data = [
            {"id": uid, "x": coords['x_final'], "y": coords['y_final']}
            for uid, coords in results.items()
        ]
        
        return {
            "count": len(formatted_data),
            "data": formatted_data
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)