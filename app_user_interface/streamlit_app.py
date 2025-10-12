"""
Streamlit application for AI Habit Coach.

This file connects the user interface with the source modules:
- It takes a short text journal entry and optional selfie.
- Calls text_analysis.analyze_text, emotion_analysis.analyze_face, and fusion.fuse.
- Generates feedback via feedback_generator.generate_feedback.
- Displays the results and stores the entry locally.

Run:
    streamlit run app/streamlit_app.py
"""
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



import streamlit as st
from source_code.text_analysis import analyze_text
from source_code.emotion_analysis import analyze_face
from source_code.fusion import fuse
from source_code.feedback_generator import generate_feedback
from source_code.storage import save_entry, load_entries
import pandas as pd

# Streamlit page configuration (title and layout)
st.set_page_config(page_title="AI Habit Coach", layout="centered")

st.title("💬 AI Habit Coach")
st.markdown(
    "Write a short journal entry and optionally upload a selfie. "
    "All analysis runs locally for privacy. This prototype provides supportive feedback and a simple mood tracker."
)

# Create an input form so that the user can submit text and an optional image
with st.form("input_form"):
    name = st.text_input("Your name (optional)", value="")
    text = st.text_area("How are you feeling today? (1-6 sentences)", height=150)
    uploaded_file = st.file_uploader("Optional: upload a selfie (jpg/png)", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("Analyze")

# When the user submits the form, process the inputs
if submitted:
    if not text.strip():
        st.warning("Please write something in the journal entry before analyzing.")
    else:
        # Analyze text
        with st.spinner("Analyzing text..."):
            text_result = analyze_text(text)

        # Analyze face if provided
        face_result = None
        if uploaded_file is not None:
            with st.spinner("Analyzing face (optional)..."):
                try:
                    # Streamlit file-like object can be passed directly to analyze_face
                    face_result = analyze_face(uploaded_file)
                except Exception as e:
                    st.error(f"Face analysis failed: {e}")
                    face_result = {"dominant_emotion": "no_face_detected", "score": 0.0}

        # Fuse signals and generate feedback
        fusion_result = fuse(text_result, face_result)
        feedback_obj = generate_feedback(fusion_result, text_result, face_result, name if name else None)

        # Display results to the user
        st.subheader("Summary")
        st.write(f"**Mood score:** {fusion_result['mood_score']*100:.1f}% — {fusion_result['category'].upper()}")
        st.write(f"**Text sentiment:** {text_result['label']} ({text_result['score']*100:.1f}%)")
        st.write(f"**Detected keywords:** {', '.join(text_result['keywords']) if text_result['keywords'] else '—'}")
        if face_result and face_result.get("dominant_emotion") != "no_face_detected":
            st.write(f"**Face emotion:** {face_result.get('dominant_emotion')} ({face_result.get('score')*100:.1f}%)")
        st.info(feedback_obj['feedback'])
        st.caption(feedback_obj['rationale'])

        # Save the entry locally when the analysis completes
        save_entry(text, feedback_obj, fusion_result, text_result, face_result)

# Sidebar shows mood history
st.sidebar.header("Mood Tracker")
entries = load_entries()

if entries:
    # Convert each SQLAlchemy Entry object to a plain dictionary
    data = []
    for e in entries:
        data.append({
            "timestamp": e.timestamp,
            "text": e.text,
            "text_emotion": e.text_emotion,
            "face_emotion": e.face_emotion,
            "mood_score": e.mood_score,
            "feedback": e.feedback
        })

    # Now safely create a DataFrame
    import pandas as pd
    df = pd.DataFrame(data)

    # Convert timestamp column to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Display mood trend chart
    st.line_chart(df.set_index("timestamp")["mood_score"])
else:
    st.info("No entries yet. Write your first journal entry above! 🌱")

