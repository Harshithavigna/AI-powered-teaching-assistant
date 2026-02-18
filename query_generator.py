import pandas as pd
import random

# Define Topics, Intents, and Difficulties
TOPICS = [
    "Optimization", "Neural Networks", "Natural Language Processing", 
    "Computer Vision", "Reinforcement Learning", "Backpropagation", 
    "Gradient Descent", "Transformers", "CNN", "RNN"
]

INTENTS = [
    "Explanation", "Example", "Doubt clarification", "Revision"
]

DIFFICULTIES = [
    "Beginner", "Intermediate", "Advanced"
]

# Templates for synthetic generation
TEMPLATES = {
    "Explanation": [
        "What is {topic}?",
        "Explain different types of {topic}.",
        "I don't understand {topic}.",
        "Can you describe {topic}?",
        "Tell me about {topic}.",
        "Define {topic}.",
        "How does {topic} work?",
        "Meaning of {topic}?",
    ],
    "Example": [
        "Give me an example of {topic}.",
        "Show me a use case for {topic}.",
        "Practical application of {topic}?",
        "Demonstrate {topic} with an example.",
        "Code example for {topic}.",
        "Real world example of {topic}.",
    ],
    "Doubt clarification": [
        "Why do we use {topic}?",
        "What is the difference between {topic} and other method?",
        "Is {topic} better than others?",
        "I am stuck on {topic}.",
        "Why does {topic} fail?",
        "Confusion about {topic}.",
        "Clarify {topic} for me.",
    ],
    "Revision": [
        "Revise {topic} quickly.",
        "Summary of {topic}.",
        "Key points of {topic}.",
        "Recap {topic}.",
        "Review {topic}.",
        "Important concepts in {topic}.",
    ]
}

def generate_query(topic, intent, difficulty):
    template = random.choice(TEMPLATES[intent])
    query = template.format(topic=topic)
    
    # Add some noise or variation based on difficulty (simple heuristic)
    if difficulty == "Beginner":
        query = query + " keep it simple."
    elif difficulty == "Advanced":
        query = query + " in depth detail."
        
    return query

def generate_dataset(num_samples=1000):
    data = []
    
    for _ in range(num_samples):
        topic = random.choice(TOPICS)
        intent = random.choice(INTENTS)
        difficulty = random.choice(DIFFICULTIES)
        
        query = generate_query(topic, intent, difficulty)
        
        data.append({
            "query": query,
            "intent": intent,
            "topic": topic,
            "difficulty": difficulty
        })
        
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_dataset(2000)
    output_path = "data/synthetic_queries.csv"
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} queries and saved to {output_path}")
