# 🌿 AI Habit Coach  

**AI Habit Coach** is a local, privacy-first AI assistant that helps you reflect on your daily emotions and habits.  
Write a short journal entry (and optionally upload a selfie), and the app will:  

- 🧠 Analyze your **text** sentiment and emotional tone using NLP  
- 😊 Detect your **facial emotion** (optional, from an image)  
- 🎯 Fuse both signals into a **combined mood score**  
- 💬 Generate **personalized, empathetic feedback**  
- 📊 Store your entries and visualize your **emotional trends over time**  

Built entirely in **Python**, powered by **Streamlit**, **Hugging Face Transformers**, **FER**, and **SQLAlchemy (SQLite)**.  
Runs 100% locally : your data never leaves your computer.

---

## 🚀 Demo Preview

![Demo Screenshot](https://via.placeholder.com/800x400?text=AI+Habit+Coach+App+Preview)

> _"Reflect, analyze, and grow — one day at a time."_

---

## 🧩 Project Structure

Here’s how the AI Habit Coach project is organized:

```text
AI-habit-coach/
│
├── app/
│   └── streamlit_app.py           # Streamlit web interface
│
├── src/
│   ├── text_analysis.py           # NLP emotion & sentiment detection
│   ├── emotion_analysis.py        # Facial emotion recognition
│   ├── fusion.py                  # Combines text + image emotion signals
│   ├── feedback_generator.py      # Generates personalized feedback
│   └── storage.py                 # Local database (SQLite) for entries
│
├── tests/
│   └── test_fusion.py             # Unit test for the fusion module
│
├── data/
│   └── entries.db                 # Auto-created SQLite database (local)
│
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions workflow for automatic testing
│
├── requirements.txt               # Dependencies
├── Dockerfile                     # For containerized deployment
├── README.md                      # Project overview (this file)
                   
