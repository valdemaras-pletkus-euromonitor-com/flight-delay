"""
FastAPI server for flight delay prediction.

This server provides APIs to:
1. Predict flight delay probability based on day of week and airport ID
2. Return a list of all airports sorted alphabetically

The model predicts the probability of arrival delays (>15 minutes) using
a logistic regression model trained on FAA flight data.
"""

import pickle
import csv
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Flight Delay Prediction API",
    description="API for predicting flight delays and retrieving airport information",
    version="1.0.0"
)

# Add CORS middleware to handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Response models
class PredictionResponse(BaseModel):
    delay_probability: float
    confidence: float

class Airport(BaseModel):
    id: int
    name: str

# Load the trained model
try:
    with open('flight_delay_model.pkl', 'rb') as file:
        model = pickle.load(file)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Load airports data
def load_airports() -> List[Dict[str, any]]:
    """Load airports from CSV file and return as list of dictionaries"""
    airports = []
    try:
        with open('airports.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                airports.append({
                    'id': int(row['AirportID']),
                    'name': row['AirportName']
                })
        # Sort alphabetically by name
        airports.sort(key=lambda x: x['name'])
        return airports
    except Exception as e:
        print(f"Error loading airports: {e}")
        return []

@app.get("/predict", response_model=PredictionResponse)
async def predict_delay(day_of_week: int, airport_id: int):
    """
    Predict flight delay probability.
    
    Args:
        day_of_week (int): Day of week (1=Monday, 2=Tuesday, ..., 7=Sunday)
        airport_id (int): Airport ID from the airports dataset
    
    Returns:
        PredictionResponse: Contains delay probability and confidence
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model not available")
    
    if not 1 <= day_of_week <= 7:
        raise HTTPException(status_code=400, detail="day_of_week must be between 1 and 7")
    
    try:
        # Make prediction using the model
        prediction = model.predict_proba([[day_of_week, airport_id]])[0]
        
        # prediction[0] is probability of no delay (class 0)
        # prediction[1] is probability of delay (class 1)
        delay_probability = float(prediction[1])
        no_delay_probability = float(prediction[0])
        
        # Confidence is the maximum probability (how confident the model is)
        confidence = float(max(prediction))
        
        return PredictionResponse(
            delay_probability=delay_probability,
            confidence=confidence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/airports", response_model=List[Airport])
async def get_airports():
    """
    Get list of all airports sorted alphabetically by name.
    
    Returns:
        List[Airport]: List of airports with ID and name
    """
    airports_data = load_airports()
    if not airports_data:
        raise HTTPException(status_code=500, detail="Unable to load airports data")
    
    return [Airport(id=airport['id'], name=airport['name']) for airport in airports_data]

@app.get("/")
async def root():
    """Root endpoint providing API information"""
    return {
        "message": "Flight Delay Prediction API",
        "endpoints": {
            "/predict": "Predict flight delay probability (requires day_of_week and airport_id parameters)",
            "/airports": "Get list of all airports sorted alphabetically"
        }
    }