from models.nlp_module import QueryUnderstandingModel
from models.adaptive_module import AdaptiveLearningModel

def train_all():
    print("=== Training NLP Model ===")
    nlp_model = QueryUnderstandingModel()
    nlp_model.train("data/synthetic_queries.csv")
    
    print("\n=== Training Adaptive Learning Model ===")
    adaptive_model = AdaptiveLearningModel()
    adaptive_model.train("data/synthetic_interactions.csv")
    
    print("\nAll models trained successfully!")

if __name__ == "__main__":
    train_all()
