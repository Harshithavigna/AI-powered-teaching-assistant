import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class AdaptiveLearningModel:
    def __init__(self, model_dir='models/saved_models'):
        self.model_dir = model_dir
        
        # Classifiers for each target
        self.next_topic_clf = RandomForestClassifier(n_estimators=100, random_state=42)
        self.action_clf = RandomForestClassifier(n_estimators=100, random_state=42)
        self.difficulty_adj_clf = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # Encoders
        self.topic_encoder = LabelEncoder()
        self.difficulty_encoder = LabelEncoder()
        self.next_topic_encoder = LabelEncoder()
        self.action_encoder = LabelEncoder()
        self.difficulty_adj_encoder = LabelEncoder()
        
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

    def train(self, data_path):
        print("Loading interaction data...")
        df = pd.read_csv(data_path)
        
        # Preprocessing
        print("Preprocessing data...")
        # Encode categorical features
        df['topic_enc'] = self.topic_encoder.fit_transform(df['topic'])
        df['difficulty_enc'] = self.difficulty_encoder.fit_transform(df['difficulty'])
        
        # Features: Current state
        X = df[['topic_enc', 'difficulty_enc', 'score', 'attempts', 'time_spent']]
        
        # Targets
        y_next_topic = self.next_topic_encoder.fit_transform(df['next_topic'])
        y_action = self.action_encoder.fit_transform(df['next_action'])
        y_diff_adj = self.difficulty_adj_encoder.fit_transform(df['next_difficulty_adj'])
        
        print("Training Next Topic Classifier...")
        self.next_topic_clf.fit(X, y_next_topic)
        
        print("Training Action Classifier...")
        self.action_clf.fit(X, y_action)
        
        print("Training Difficulty Adjustment Classifier...")
        self.difficulty_adj_clf.fit(X, y_diff_adj)
        
        print("Saving adaptive models...")
        self.save_models()
        print("Adaptive learning training complete.")

    def predict(self, current_topic, current_difficulty, score, attempts, time_spent):
        # Encode inputs
        try:
            topic_enc = self.topic_encoder.transform([current_topic])[0]
            diff_enc = self.difficulty_encoder.transform([current_difficulty])[0]
        except ValueError as e:
            # Debugging: return valid options
            valid_topics = list(self.topic_encoder.classes_)
            valid_diffs = list(self.difficulty_encoder.classes_)
            return {
                "error": f"Unknown inputs. Valid Topics: {valid_topics[:3]}... Valid Difficulties: {valid_diffs}. Error: {str(e)}"
            }
            
        features = np.array([[topic_enc, diff_enc, score, attempts, time_spent]])
        
        # Predict with probabilities
        next_topic_enc = self.next_topic_clf.predict(features)[0]
        next_topic_prob = np.max(self.next_topic_clf.predict_proba(features)[0])
        
        action_enc = self.action_clf.predict(features)[0]
        action_prob = np.max(self.action_clf.predict_proba(features)[0])
        
        diff_adj_enc = self.difficulty_adj_clf.predict(features)[0]
        diff_adj_prob = np.max(self.difficulty_adj_clf.predict_proba(features)[0])
        
        # Decode
        next_topic = self.next_topic_encoder.inverse_transform([next_topic_enc])[0]
        action = self.action_encoder.inverse_transform([action_enc])[0]
        diff_adj = self.difficulty_adj_encoder.inverse_transform([diff_adj_enc])[0]
        
        # Generate Reasoning
        reasoning = []
        if score < 50:
            reasoning.append(f"Score ({score}%) suggests need for reinforcement.")
        elif score > 80:
            reasoning.append(f"High score ({score}%) indicates mastery.")
            
        if attempts > 2 and score < 60:
            reasoning.append(f"Multiple attempts ({attempts}) with low score.")
            
        if not reasoning:
            reasoning.append("Standard progression based on curriculum.")
            
        return {
            "next_topic": next_topic,
            "next_topic_conf": round(next_topic_prob * 100),
            "action": action,
            "action_conf": round(action_prob * 100),
            "difficulty_adjustment": diff_adj,
            "difficulty_adjustment_conf": round(diff_adj_prob * 100),
            "reasoning": " ".join(reasoning)
        }

    def save_models(self):
        with open(f"{self.model_dir}/adaptive_models.pkl", "wb") as f:
            pickle.dump({
                "next_topic_clf": self.next_topic_clf,
                "action_clf": self.action_clf,
                "difficulty_adj_clf": self.difficulty_adj_clf,
                "encoders": {
                    "topic": self.topic_encoder,
                    "difficulty": self.difficulty_encoder,
                    "next_topic": self.next_topic_encoder,
                    "action": self.action_encoder,
                    "difficulty_adj": self.difficulty_adj_encoder
                }
            }, f)

    def load_models(self):
        try:
            with open(f"{self.model_dir}/adaptive_models.pkl", "rb") as f:
                data = pickle.load(f)
                self.next_topic_clf = data["next_topic_clf"]
                self.action_clf = data["action_clf"]
                self.difficulty_adj_clf = data["difficulty_adj_clf"]
                self.topic_encoder = data["encoders"]["topic"]
                self.difficulty_encoder = data["encoders"]["difficulty"]
                self.next_topic_encoder = data["encoders"]["next_topic"]
                self.action_encoder = data["encoders"]["action"]
                self.difficulty_adj_encoder = data["encoders"]["difficulty_adj"]
            print("Adaptive models loaded successfully.")
            return True
        except FileNotFoundError:
            print("Saved adaptive models not found. Please train first.")
            return False

if __name__ == "__main__":
    # Example usage
    model = AdaptiveLearningModel()
    # model.train("../data/synthetic_interactions.csv")
