"""
Basic unit tests for the fusion module.
Run with: pytest
"""

from source_code.fusion import fuse

def test_fusion_range_and_category():
    # Provide synthetic test inputs to ensure the function runs and returns valid outputs
    text_input = {"valence": 0.8, "motivation_score": 0.3}
    face_input = {"dominant_emotion": "happy", "score": 0.8}
    res = fuse(text_input, face_input)
    assert 0.0 <= res["mood_score"] <= 1.0
    assert res["category"] in ["low", "medium", "high"]
