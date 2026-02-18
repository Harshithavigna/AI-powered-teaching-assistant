# AI Teaching Assistant - AU Campus Recruitment 2026

## Overview
This project is an AI-powered teaching assistant designed to:
1.  **Understand Student Queries**: Classifies intent, topic, and difficulty of student questions using NLP.
2.  **Recommend Learning Paths**: Adapts the learning path (Next Topic, Action, Difficulty) based on student performance using a Machine Learning model.

## Setup Instructions

### Prerequisites
- Python 3.9+
- pip

### Installation
1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd au_campus_recruitment_2026
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Data Generation
Since no external dataset was provided, this project uses synthetic data generation scripts to create localized, relevant training data.
1.  Generate Query Dataset:
    ```bash
    python data_gen/query_generator.py
    ```
2.  Generate Interaction Dataset:
    ```bash
    python data_gen/interaction_generator.py
    ```
    *Note: Data is saved to `data/` directory.*

## Training Models
Train both the NLP and Adaptive Learning models:
```bash
python train.py
```
*This will save trained models to `models/saved_models/`.*

## Running the Demo

### Web Interface (Recommended)
Start the modern web application:
```bash
uvicorn app:app --reload
```
Then open your browser and navigate to: **http://127.0.0.1:8000**

### CLI Interface (Legacy)
Start the interactive command-line interface:
```bash
python main.py
```

## Project Structure
- `app.py`: FastAPI backend for the web interface.
- `static/` & `templates/`: Frontend assets (HTML, CSS, JS).
- `data_gen/`: Scripts for generating synthetic training data.
- `models/`: ML models for NLP and Adaptive Learning.
- `train.py`: Orchestrates the training process.
- `main.py`: CLI for user interaction.

## Assumptions
- **Synthetic Data**: The models are trained on synthetic data which mimics real-world student interactions but may lack the nuance of large-scale real datasets.
- **State Space**: The adaptive model assumes a simplified state space (Topic, Score, Attempts, Time) to make decisions.
