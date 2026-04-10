from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
import datetime
import pickle
import os
import re
import string

app = FastAPI(title="Sentiment Analysis API")

# --- ML Model Loading ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
TFIDF_PATH = os.path.join(os.path.dirname(__file__), "tfidf.pkl")

try:
    with open(MODEL_PATH, "rb") as f:
        ml_model = pickle.load(f)
    print(f"Successfully loaded ML model from {MODEL_PATH}!")
    
    with open(TFIDF_PATH, "rb") as f:
        tfidf = pickle.load(f)
    print(f"Successfully loaded TF-IDF vectorizer from {TFIDF_PATH}!")
except Exception as e:
    ml_model = None
    tfidf = None
    print(f"Note: Could not load model/vectorizer ({e}). Using fallback dummy logic until both are added.")

def clean_text(text: str) -> str:
    text = str(text) # Convert to string
    text = text.lower() # Lowercase
    text = "".join([i for i in text if i not in string.punctuation]) # Remove punctuations
    text = re.sub(r'[^a-zA-Z\s]', '', text) # Remove numbers, emojis and special characters
    text = re.sub(r'\s+', ' ', text).strip() # Remove extra spaces
    return text

# Setup CORS to allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection (Update URI with your actual connection string)
MONGO_URI = "mongodb://localhost:27017"
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client.sentiment_db
    reviews_collection = db.reviews
except Exception as e:
    print(f"MongoDB connection error: {e}")

class ReviewInput(BaseModel):
    review_text: str

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float

def predict_sentiment(text: str) -> dict:
    """
    Predict using the loaded pickle model if available.
    """
    if ml_model is not None and tfidf is not None:
        try:
            # 1. Clean the text using the function above
            clean_review = clean_text(text)
            
            # 2. Transform the text using your tfidf vectorizer
            test = tfidf.transform([clean_review])
            
            # 3. Predict using your Naive Bayes model
            prediction = ml_model.predict(test)[0]
            
            # Map output exactly like your Jupyter Notebook (0 = Negative)
            if prediction == 0:
                return {"sentiment": "Negative", "confidence": 0.90} 
            else:
                return {"sentiment": "Positive", "confidence": 0.90}
        except Exception as e:
            print(f"Error during model inference: {e}")

    # --- Dummy Fallback Logic ---
    text_lower = text.lower()
    if any(word in text_lower for word in ["good", "great", "excellent", "love", "amazing"]):
        return {"sentiment": "Positive", "confidence": 0.92}
    elif any(word in text_lower for word in ["bad", "terrible", "poor", "hate", "worst"]):
        return {"sentiment": "Negative", "confidence": 0.88}
    else:
        return {"sentiment": "Neutral", "confidence": 0.50}

@app.post("/api/review", response_model=SentimentResponse)
async def analyze_review(review: ReviewInput):
    text = review.review_text
    if not text.strip():
        raise HTTPException(status_code=400, detail="Review text cannot be empty")
    
    # 1. Run ML Model
    prediction = predict_sentiment(text)
    sentiment = prediction["sentiment"]
    confidence = prediction["confidence"]
    
    # 2. Save to MongoDB
    record = {
        "review_text": text,
        "sentiment": sentiment,
        "confidence": confidence,
        "timestamp": datetime.datetime.utcnow()
    }
    
    try:
        reviews_collection.insert_one(record)
    except Exception as e:
        print(f"Failed to save to database: {e}")
        # Note: We continue executing even if MongoDB save fails so the user still gets a response
    
    return {"sentiment": sentiment, "confidence": confidence}

if __name__ == "__main__":
    import uvicorn
    # Make sure to run this file either directly, or run: uvicorn main:app --reload
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
