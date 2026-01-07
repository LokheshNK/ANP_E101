import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from engine.nlp_filter import analyze_communication
from engine.scoring import process_metrics

app = FastAPI()

# Enable CORS for React integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve path for the data file
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "mock_data.json")

@app.get("/api/dashboard")
async def get_dashboard():
    # Load raw data
    with open(DATA_PATH, 'r') as f:
        raw_data = json.load(f)
    
    # Run NLP filtering on the messages
    for user in raw_data:
        user['comm_score'] = analyze_communication(user['msgs'])
    
    # Run Scoring Engine
    final_data = process_metrics(raw_data)
    
    return final_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)