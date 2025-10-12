"""
Template-based feedback generator.

Rationale:
- We avoid open-ended generative models (LLMs) here for safety and reproducibility.
- Templates produce consistent, controlled responses ideal for wellbeing support prototypes.

Outputs:
- feedback: a friendly sentence to the user
- rationale: a short transparent explanation about why the suggestion was made
"""

import random

# Templates for each mood category
TEMPLATES = {
    "low": [
        "I’m sorry you’re having a tough time. Small steps can help — try {micro_action}.",
        "That sounds rough. Consider taking a brief break and doing {micro_action} to reset a little."
    ],
    "medium": [
        "You're doing okay. Keep building momentum with {micro_action}.",
        "Nice awareness — try {micro_action} today to stay consistent."
    ],
    "high": [
        "Great energy! Keep it up — maybe {micro_action} as a small challenge.",
        "You seem in a good mood. Consider {micro_action} to stretch your progress a little."
    ]
}

# Small, evidence-informed micro-actions (easy to perform)
MICRO_ACTIONS = [
    "a 10-minute walk",
    "a short breathing exercise",
    "writing one thing you’re grateful for",
    "a focused 20-minute session on a small task",
    "listening to a favorite song"
]

def pick_micro_action():
    """Return a random small, doable action for the user."""
    return random.choice(MICRO_ACTIONS)

def generate_feedback(fusion_result, text_analysis, face_analysis=None, name=None):
    """
    Create a feedback message and a rationale string.

    Inputs:
      - fusion_result: output of fuse() containing mood_score & category
      - text_analysis: output of analyze_text()
      - face_analysis: optional output of analyze_face()

    Returns:
      {
        "feedback": "...",
        "rationale": "..."
      }
    """
    category = fusion_result.get("category", "medium")
    template = random.choice(TEMPLATES.get(category, TEMPLATES["medium"]))
    micro = pick_micro_action()

    # Slight personalization: if user mentioned a keyword, sometimes tie the micro-action to it.
    keywords = text_analysis.get("keywords", [])
    if keywords and random.random() < 0.4:
        micro = f"{micro} related to {keywords[0]}"

    feedback_text = template.format(micro_action=micro)

    # Rationale: transparent explanation for the user and interviewers alike.
    rationale = f"({int(fusion_result['mood_score'] * 100)}% mood score based on your words"
    if face_analysis and face_analysis.get("dominant_emotion") != "no_face_detected":
        rationale += f" and detected face emotion '{face_analysis.get('dominant_emotion')}'"
    rationale += ")"

    return {"feedback": feedback_text, "rationale": rationale}
