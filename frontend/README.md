# Flight Delay Predictor Frontend

A simple, responsive web application that predicts flight delay probabilities using the Flight Delay Prediction API.

## Features

- **Day Selection**: Choose from Monday through Sunday (mapped to values 1-7)
- **Airport Selection**: Dynamically loaded list of airports sorted alphabetically
- **Real-time Predictions**: Calls the API and displays delay probability and model confidence
- **Responsive Design**: Clean, user-friendly interface that works on different screen sizes
- **Error Handling**: Graceful handling of API errors and invalid inputs

## How to Use

1. **Start the API Server**: Make sure the FastAPI server is running on port 8000
   ```bash
   cd /path/to/flight-delay
   uvicorn server.main:app --host 0.0.0.0 --port 8000
   ```

2. **Serve the Frontend**: Start a simple HTTP server
   ```bash
   cd frontend
   python -m http.server 8080
   ```

3. **Open in Browser**: Navigate to `http://localhost:8080`

4. **Make Predictions**:
   - Select a day of the week
   - Choose an airport from the dropdown
   - Click "Predict Delay Probability"
   - View the results showing delay probability and model confidence

## API Dependencies

The frontend requires the following API endpoints:
- `GET /airports` - Returns list of airports with id and name
- `GET /predict?day_of_week={1-7}&airport_id={id}` - Returns delay prediction

## Technical Details

- **Framework**: Pure HTML/JavaScript (no dependencies)
- **Styling**: Custom CSS with modern, responsive design
- **CORS**: API server includes CORS middleware for cross-origin requests
- **Error Handling**: User-friendly error messages for API failures
- **Loading States**: Visual feedback during API calls

## Example Output

The application displays predictions in the format:
- **Flight Details**: Day and airport name
- **Delay Probability**: Percentage chance of delay >15 minutes  
- **Model Confidence**: How confident the ML model is in its prediction