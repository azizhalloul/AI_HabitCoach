"""
Text analysis utilities for AI Habit Coach.

This module:
- Instantiates a Hugging Face 'sentiment-analysis' pipeline (DistilBERT).
- Provides analyze_text(text) that returns sentiment label/score and
  a small heuristic 'motivation_score' plus keywords for personalization.

Why:
- Using a pretrained model speeds development and provides robust results
  for short text entries typical of a user's journal.
"""

from transformers import pipeline
import re

# Lazy-initialized pipeline to avoid reloading the model on every call.
_sentiment_pipe = None

def get_sentiment_pipeline():
    """
    Return a singleton sentiment-analysis pipeline.
    The pipeline loads the model into memory the first time it is called.
    """
    global _sentiment_pipe
    if _sentiment_pipe is None:
        # Use a compact, well-known fine-tuned model for sentiment tasks.
        _sentiment_pipe = pipeline( "sentiment-analysis",
                                    model="distilbert-base-uncased-finetuned-sst-2-english")
    return _sentiment_pipe

def analyze_text(text):
    """
    Analyze the input text and return a structured dict with:
      - label: "POSITIVE" or "NEGATIVE"
      - score: confidence of the label (0..1)
      - valence: numeric sentiment [0..1], where larger is more positive
      - motivation_score: heuristic [0..1] that detects activity-related words
      - keywords: list of found motivational keywords

    Why:
    - Valence gives a numeric signal for fusion with face emotion.
    - Motivation_score helps produce tailored advice when the user mentions goals.
    """
    pipe = get_sentiment_pipeline()
    # Truncate input to model-friendly size: pipeline will tokenize and process.
    result = pipe(text[:512])[0]  # returns a dict like {"label": "...", "score": 0.99}
    label = result["label"]
    score = float(result["score"])

    # Simple heuristic keywords indicating motivation/intent to act.
    motivation_keywords = [
        "goal", "plan", "exercise", "workout", "study",
        "read", "practice", "build", "apply", "learn", "finish"
    ]
    text_lower = text.lower()
    found = [kw for kw in motivation_keywords if re.search(rf"\b{kw}\b", text_lower)]

    # Build a simple motivation score: more keywords → higher score.
    motivation_score = min(1.0, 0.2 * len(found) + (0.3 if label == "POSITIVE" else 0.0))

    # Convert label to numeric valence (POSITIVE -> score, NEGATIVE -> 1 - score)
    valence = score if label == "POSITIVE" else (1 - score)

    return {
        "label": label,
        "score": score,
        "valence": valence,
        "motivation_score": motivation_score,
        "keywords": found }

if __name__ == "__main__":
    sample_text = "I feel happy and excited today!"
    result = analyze_text(sample_text)  # replace with your function name
    print("Text Analysis Result:", result)

