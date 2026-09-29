# 🎬 CineMind — AI Movie Recommendation System

CineMind is an AI-powered movie recommendation system that helps users discover movies based on natural-language queries.

Users can describe what they want, for example:

> "I want a sci-fi movie like Interstellar with a rating above 7 and under 180 minutes."

CineMind analyzes the request, extracts the user's preferences, and recommends relevant movies using a content-based recommendation algorithm.

---

## 🚀 Features

- 🎬 Movie recommendation system
- 🔍 Natural-language movie queries
- 🧠 TF-IDF based content recommendation
- 📐 Cosine similarity for movie similarity
- 🔤 Fuzzy movie-title matching using RapidFuzz
- 🎭 Genre filtering
- ⭐ Rating filtering
- ⏱ Runtime filtering
- 📅 Release-year filtering
- ⚡ FastAPI backend
- 🌐 Modern web interface
- 📚 Automatic API documentation with Swagger
- 💾 Saved ML model components for faster startup

---

## 🧠 How It Works

The recommendation pipeline works as follows:

```text
User Query
     ↓
Natural Language Query Parser
     ↓
Extract Preferences
     ↓
Genre / Rating / Runtime / Year Filters
     ↓
Find Reference Movie
     ↓
TF-IDF Representation
     ↓
Cosine Similarity
     ↓
Rank Similar Movies
     ↓
Movie Recommendations