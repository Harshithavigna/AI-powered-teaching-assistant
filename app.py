import sys
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.nlp_module import QueryUnderstandingModel
from models.adaptive_module import AdaptiveLearningModel

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Load Models
print("Loading models...")
try:
    nlp_model = QueryUnderstandingModel()
    if not nlp_model.load_models():
        print("Warning: NLP models not found. Predictions will fail.")

    adaptive_model = AdaptiveLearningModel()
    if not adaptive_model.load_models():
        print("Warning: Adaptive models not found. Recommendations will fail.")
except Exception as e:
    print(f"Error loading models: {e}")

# Pydantic Models for API
class QueryRequest(BaseModel):
    query: str

class AdaptiveRequest(BaseModel):
    topic: str
    difficulty: str
    score: float
    attempts: int
    time_spent: float

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/analyze")
async def analyze_query(request: QueryRequest):
    if not request.query:
        return {"error": "Query cannot be empty"}
    
    try:
        result = nlp_model.predict(request.query)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/recommend")
async def recommend_path(request: AdaptiveRequest):
    try:
        recommendation = adaptive_model.predict(
            request.topic, 
            request.difficulty, 
            request.score, 
            request.attempts, 
            request.time_spent
        )
        return recommendation
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
