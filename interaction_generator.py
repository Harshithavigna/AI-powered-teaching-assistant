import pandas as pd
import random
import numpy as np

TOPICS = [
    "Optimization", "Neural Networks", "NLP", "Computer Vision", "RL", 
    "Backpropagation", "Gradient Descent", "Transformers", "CNN", "RNN"
]

DIFFICULTY_LEVELS = ["Beginner", "Intermediate", "Advanced"]

def simulate_student_history(student_id, steps=20):
    history = []
    current_topic_idx = 0
    current_difficulty_idx = 0
    
    for _ in range(steps):
        topic = TOPICS[current_topic_idx]
        difficulty = DIFFICULTY_LEVELS[current_difficulty_idx]
        
        # Simulate Score based on noise and some underlying proficiency
        # Assume proficiency increases over time
        proficiency = min(0.9, 0.3 + 0.05 * _) 
        
        # Score is lower for higher difficulties
        difficulty_penalty = current_difficulty_idx * 0.2
        
        score = min(100, max(0, int(np.random.normal(loc=(proficiency - difficulty_penalty) * 100, scale=15))))
        
        time_spent = random.randint(5, 60) # minutes
        attempts = random.randint(1, 4)
        
        # Determine Next Action (Rule based ground truth for training/imitation)
        next_topic = topic
        next_action = "Continue" 
        difficulty_adj = "Same"
        
        if score > 80:
            if current_difficulty_idx < 2:
                difficulty_adj = "Increase"
                current_difficulty_idx += 1
            else:
                next_action = "Next Topic"
                current_topic_idx = (current_topic_idx + 1) % len(TOPICS) # Move to next topic
                current_difficulty_idx = 0 # Reset difficulty for new topic
        elif score < 50:
             next_action = "Revision"
             if current_difficulty_idx > 0:
                 difficulty_adj = "Decrease"
                 current_difficulty_idx -= 1
        
        history.append({
            "student_id": student_id,
            "topic": topic,
            "difficulty": difficulty,
            "score": score,
            "attempts": attempts,
            "time_spent": time_spent,
            "next_topic": TOPICS[current_topic_idx], # Potentially changed
            "next_action": next_action,
            "next_difficulty_adj": difficulty_adj
        })
        
    return history

def generate_interaction_dataset(num_students=50):
    all_data = []
    for i in range(num_students):
        student_history = simulate_student_history(student_id=f"S{i:03d}")
        all_data.extend(student_history)
        
    return pd.DataFrame(all_data)

if __name__ == "__main__":
    df = generate_interaction_dataset(100)
    output_path = "data/synthetic_interactions.csv"
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} interactions and saved to {output_path}")
