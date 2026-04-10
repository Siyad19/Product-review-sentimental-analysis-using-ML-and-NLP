# Product Review Sentiment Analyzer

Hey there! 👋 Welcome to my Sentiment Analysis project. 

This is an end-to-end AI application I built to figure out whether customer product reviews are **Positive** or **Negative**. At the core of it, I trained my own Machine Learning model (Multinomial Naive Bayes) from scratch using an Amazon reviews dataset. 

Instead of just leaving the model sitting in a Jupyter Notebook, I decided to bring it to life! I wrapped the model in a custom Python (FastAPI) backend and built a sleek, dark-themed website so users can actually type in reviews and see the AI work in real-time. On top of that, every single review and prediction is saved straight into a MongoDB database so I can visualize all the data later in Power BI.

---

## 🛠️ What I Used (Tech Stack)

* **The Brains (Machine Learning):** Python, Scikit-Learn (TF-IDF for text vectorization & Naive Bayes for classification).
* **The Engine (Backend):** FastAPI (super fast & great for ML) and Uvicorn.
* **The Memory (Database):** MongoDB (via `pymongo`).
* **The Looks (Frontend):** Plain old HTML, CSS, and JavaScript to handle the API calls.

---

## 📁 How the Files are Organized

Here is a quick map of the project folders:

```text
Product review sentimental analysis/
│
├── backend/
│   ├── main.py               # The main Python API server
│   ├── requirements.txt      # The Python packages you need to install
│   ├── model.pkl             # My trained Naive Bayes model
│   └── tfidf.pkl             # My TF-IDF text vectorizer
│
├── frontend/
│   ├── index.html            # The skeleton of the webpage
│   ├── style.css             # All the animations and dark-mode styling
│   └── script.js             # The JavaScript that talks to the backend
│
└── model/
    ├── Amazon_review_dataset.csv                   # The raw Amazon data used for training
    └── Product_review_sentimental_analysis.ipynb   # My Jupyter Notebook with the model training code
```

---

## 🚀 Want to run it yourself?

If you downloaded this and want to try it out on your machine, here is how to get it running:

### 1. Database Setup
First, make sure you have MongoDB installed and running on your computer (port `27017`). You don't need to manually create any tables—my backend will automatically create the `sentiment_db` database for you as soon as it runs!

### 2. Exporting the Models
If you decide to tweak the model inside the Jupyter Notebook, don't forget to export your new weights! Run this snippet at the bottom of the notebook to save the `.pkl` files, and drop them into the `backend/` folder:
```python
import pickle

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
    
with open('tfidf.pkl', 'wb') as f:
    pickle.dump(tfidf, f)
```

### 3. Start up the Backend
Open up your terminal (or Anaconda prompt), navigate into the `backend` folder, and run these commands to install the dependencies and boot up the server:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
Once it says `Successfully loaded ML model & TF-IDF Vectorizer!`, you are good to go.

### 4. Open the Website!
You don't even need a fancy web server for the frontend. Just open up the `frontend/` folder and double-click `index.html` to load it in your browser. Type in a review, hit analyze, and watch the AI do its thing!

---

## 📈 Power BI Integration
Because everything is saved to MongoDB, hooking it up to a dashboard is super easy:
1. Open **MongoDB Compass** and connect to your local database (`mongodb://localhost:27017`).
2. Find the `sentiment_db` database, open the `reviews` collection, and click "Export Data" to grab it as a CSV.
3. Drop that CSV into **Power BI**, and you can instantly build cool visuals like sentiment pie charts or average confidence score gauges!