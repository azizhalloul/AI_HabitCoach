"""
Facial emotion detection utilities using the FER library.

This module:
- Instantiates a FER detector (with MTCNN face detection enabled).
- Provides analyze_face(image_file) to detect the dominant face emotion.

Notes:
- The function accepts:
    - a file-like object (Streamlit upload),
    - a PIL.Image instance, or
    - a filesystem path string.
- Returns a dict with 'dominant_emotion', 'score', and 'raw' results.
- If no face is detected, returns 'no_face_detected' with score 0.0.
"""

from fer import FER
import numpy as np
from PIL import Image

# Single shared detector instance for efficiency.
_detector = None

def get_detector():
    """
    Lazy-initialize and return the FER detector.
    mtcnn=True uses a robust face detector which improves detection in real photos.
    """
    global _detector
    if _detector is None:
        _detector = FER(mtcnn=True)
    return _detector

def pil_to_cv2(img_pil):
    """
    Convert a PIL Image to an OpenCV-style numpy array (BGR).
    FER expects a numpy array in BGR order.
    """
    img = np.array(img_pil.convert('RGB'))  # convert to RGB numpy
    # Convert RGB to BGR by reversing the last axis
    return img[:, :, ::-1].copy()

def analyze_face(image_file):
    """
    Detect emotions in the given image.
    Input: file-like object (has .read), PIL.Image, or path string.

    Returns:
      {
        "dominant_emotion": str,
        "score": float,
        "raw": list  # raw FER detection results (could be empty)
      }
    """
    detector = get_detector()

    # Accept different input types gracefully
    if hasattr(image_file, "read"):
        # file-like object (e.g., Streamlit uploaded file)
        img = Image.open(image_file)
    elif isinstance(image_file, Image.Image):
        img = image_file
    else:
        # assume a filesystem path (string)
        img = Image.open(image_file)

    # Convert image to OpenCV format and run FER detector
    cv_img = pil_to_cv2(img)
    results = detector.detect_emotions(cv_img)  # list of face detections

    if not results:
        # No face detected — handle gracefully
        return {"dominant_emotion": "no_face_detected", "score": 0.0, "raw": results}

    # Choose the face with the largest bounding-box area (likely the primary face)
    best = max(results, key=lambda r: r["box"][2] * r["box"][3])
    emotions = best["emotions"]
    # dominant emotion is the one with highest probability
    dominant = max(emotions.items(), key=lambda kv: kv[1])
    return {"dominant_emotion": dominant[0], "score": float(dominant[1]), "raw": results}
