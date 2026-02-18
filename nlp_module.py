import pandas as pd
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

class QueryUnderstandingModel:
    def __init__(self, model_name='all-MiniLM-L6-v2', model_dir='models/saved_models'):
        self.model_name = model_name
        self.encoder = SentenceTransformer(model_name)
        self.model_dir = model_dir
        
        self.intent_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.topic_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.difficulty_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

    def train(self, data_path):
        print("Loading data...")
        df = pd.read_csv(data_path)
        
        print("Encoding queries...")
        embeddings = self.encoder.encode(df['query'].tolist(), show_progress_bar=True)
        
        X = embeddings
        y_intent = df['intent']
        y_topic = df['topic']
        y_difficulty = df['difficulty']
        
        print("Training Intent Classifier...")
        self.intent_classifier.fit(X, y_intent)
        
        print("Training Topic Classifier...")
        self.topic_classifier.fit(X, y_topic)
        
        print("Training Difficulty Classifier...")
        self.difficulty_classifier.fit(X, y_difficulty)
        
        print("Saving models...")
        self.save_models()
        print("Training complete.")

    def extract_keywords(self, text):
        # Simple keyword extraction (placeholder for more complex logic)
        # Remove common stopwords and return unique words > 3 chars
        stopwords = set(['what', 'is', 'the', 'how', 'to', 'in', 'of', 'and', 'a', 'an', 'for', 'explain', 'show', 'me', 'example', 'help', 'can'])
        words = text.lower().replace('?', '').replace('.', '').split()
        keywords = [w for w in words if w not in stopwords and len(w) > 2]
        return list(set(keywords))[:5] # Return top 5 unique

    def predict(self, query):
        embedding = self.encoder.encode([query])
        
        intent = self.intent_classifier.predict(embedding)[0]
        intent_prob = np.max(self.intent_classifier.predict_proba(embedding)[0])
        
        topic = self.topic_classifier.predict(embedding)[0]
        topic_prob = np.max(self.topic_classifier.predict_proba(embedding)[0])
        
        difficulty = self.difficulty_classifier.predict(embedding)[0]
        difficulty_prob = np.max(self.difficulty_classifier.predict_proba(embedding)[0])
        
        keywords = self.extract_keywords(query)
        
        # Simple rule-based suggestion
        suggestions = {
            "Explanation": "Define the concept clearly and provide a high-level overview.",
            "Example": "Provide a code snippet or a real-world analogy.",
            "Doubt clarification": "Address the specific confusion and contrast with related concepts.",
            "Revision": "Summarize key points and formulas."
        }
        suggestion = suggestions.get(intent, "Answer the query directly.")

        return {
            "intent": intent,
            "intent_conf": round(intent_prob * 100),
            "topic": topic,
            "topic_conf": round(topic_prob * 100),
            "difficulty": difficulty,
            "difficulty_conf": round(difficulty_prob * 100),
            "keywords": keywords,
            "suggestion": suggestion
        }

    def save_models(self):
        with open(f"{self.model_dir}/intent_clf.pkl", "wb") as f:
            pickle.dump(self.intent_classifier, f)
        with open(f"{self.model_dir}/topic_clf.pkl", "wb") as f:
            pickle.dump(self.topic_classifier, f)
        with open(f"{self.model_dir}/difficulty_clf.pkl", "wb") as f:
            pickle.dump(self.difficulty_classifier, f)

    def load_models(self):
        try:
            with open(f"{self.model_dir}/intent_clf.pkl", "rb") as f:
                self.intent_classifier = pickle.load(f)
            with open(f"{self.model_dir}/topic_clf.pkl", "rb") as f:
                self.topic_classifier = pickle.load(f)
            with open(f"{self.model_dir}/difficulty_clf.pkl", "rb") as f:
                self.difficulty_classifier = pickle.load(f)
            print("Models loaded successfully.")
            return True
        except FileNotFoundError:
            print("Saved models not found. Please train first.")
            return False

if __name__ == "__main__":
    # Example usage for training
    model = QueryUnderstandingModel()
    # data_path = "../data/synthetic_queries.csv"
    # model.train(data_path)
