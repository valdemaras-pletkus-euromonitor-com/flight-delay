# Flight Delay Prediction Server

This FastAPI server provides endpoints for flight delay prediction and airport information.

## Endpoints

### 1. `/predict`
Predicts flight delay probability based on day of week and airport ID.

**Parameters:**
- `day_of_week` (int): Day of week (1=Monday, 2=Tuesday, ..., 7=Sunday)
- `airport_id` (int): Airport ID from the airports dataset

**Response:**
```json
{
  "delay_probability": 0.185,
  "confidence": 0.815
}
```

**Example:**
```bash
curl "http://localhost:8000/predict?day_of_week=3&airport_id=14771"
```

### 2. `/airports`
Returns a list of all airports sorted alphabetically by name.

**Response:**
```json
[
  {"id": 10140, "name": "Albuquerque International Sunport"},
  {"id": 10423, "name": "Austin - Bergstrom International"},
  ...
]
```

**Example:**
```bash
curl "http://localhost:8000/airports"
```

## Running the Server

1. Install dependencies:
```bash
pip install fastapi uvicorn scikit-learn
```

2. Start the server:
```bash
uvicorn server.main:app --host 0.0.0.0 --port 8000
```

3. View interactive API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Model Information

The server uses a logistic regression model trained on FAA flight data to predict arrival delays (>15 minutes). The model takes two features:
- Day of week (1-7)
- Destination airport ID

The model returns probabilities for both delay and no-delay outcomes, with confidence representing the maximum probability.