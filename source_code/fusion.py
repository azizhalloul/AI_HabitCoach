"""
Multimodal fusion utilities.

This module defines a simple, interpretable fusion strategy:
- Map facial emotion labels to numeric scores.
- Combine text valence and motivation into a text component.
- Blend text and face components with weights.
- Provide a final mood_score and a categorical bucket (low/medium/high).

Why:
- Simplicity and interpretability are critical for a beginner project.
- This fusion is easy to explain to recruiters/interviewers.
"""

# Mapping from FER emotion names to approximate numeric scores (0..1).
EMOTION_TO_SCORE = {
    "angry": 0.1,
    "disgust": 0.1,
    "fear": 0.15,
    "sad": 0.2,
    "sadness": 0.2,
    "surprise": 0.6,
    "happy": 0.9,
    "neutral": 0.5,
    "no_face_detected": 0.5
}

def map_face_emotion_score(dominant_emotion, confidence):
    """
    Map a face emotion to a score in [0..1] and blend with detection confidence.
    - If confidence is high, use the mapped score.
    - If confidence is low, push closer to neutral (0.5).
    """
    base = EMOTION_TO_SCORE.get(dominant_emotion, 0.5)
    # Blend: base*confidence + neutral*(1-confidence)
    return base * confidence + 0.5 * (1 - confidence)

def fuse(text_analysis, face_analysis=None, weights=(0.6, 0.4)):
    """
    Fuse text and face signals into a single mood score.

    Inputs:
      - text_analysis: dict with keys 'valence' and 'motivation_score'
      - face_analysis: dict with keys 'dominant_emotion' and 'score' (optional)
      - weights: (weight_text, weight_face) default (0.6, 0.4)

    Returns:
      {
        "mood_score": float between 0 and 1,
        "category": "low"/"medium"/"high",
        "components": {...}
      }
    """
    # Text component: mix valence and explicit motivation
    text_val = text_analysis.get("valence", 0.5)
    text_mot = text_analysis.get("motivation_score", 0.0)
    text_comp = 0.8 * text_val + 0.2 * text_mot

    # Face component: handle missing face gracefully
    if not face_analysis or face_analysis.get("dominant_emotion") == "no_face_detected":
        face_comp = 0.5
        face_conf = 0.0
    else:
        dominant = face_analysis.get("dominant_emotion", "neutral")
        conf = face_analysis.get("score", 0.0)
        face_comp = map_face_emotion_score(dominant, conf)
        face_conf = conf

    w_text, w_face = weights
    # If face detection is unreliable, reduce its weight
    if face_conf < 0.1:
        w_text, w_face = 0.9, 0.1

    mood = w_text * text_comp + w_face * face_comp

    # Categorical bucket for easy interpretation in the UI
    if mood < 0.35:
        category = "low"
    elif mood < 0.7:
        category = "medium"
    else:
        category = "high"

    return {
        "mood_score": float(mood),
        "category": category,
        "components": {
            "text_comp": float(text_comp),
            "face_comp": float(face_comp),
            "text_valence": float(text_val),
            "motivation_score": float(text_mot)
        }
    }
