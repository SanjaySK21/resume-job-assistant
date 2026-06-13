# Semantic Resume Job Assistant

A GenAI-powered resume analyzer built with Python and Streamlit.

Upload a resume PDF and paste a job description to get:
- Semantic fit score
- Skill gap analysis
- Resume tips
- Interview questions

## Tech Stack

| Layer | Technology |
|------|-------------|
| Frontend | Streamlit |
| PDF parsing | pdfplumber |
| Skill extraction | Section-based parser + full resume fallback |
| Matching | Semantic embeddings (MiniLM) + cosine similarity |
| Embedding model | sentence-transformers (`all-MiniLM-L6-v2`) |
| AI outputs | Rule-based dynamic templates |
| Database | SQLite |
| Language | Python 3 |

## What Makes It GenAI

This project uses a transformer-based embedding model (MiniLM) to match skills by meaning, not exact string comparison.

| Scenario | Old (string match) | New (semantic match) |
|---------|---------------------|----------------------|
| "ML" vs "Machine Learning" | Miss | Match |
| "NodeJS" vs "node" | Miss | Match |
| "REST APIs" vs "rest api" | Miss | Match |
| "NLP" vs "Natural Language Processing" | Miss | Match |

## Project Structure

```text
resume-job-assistant/
├── app/
│   ├── pages/
│   │   └── 2_history.py
│   ├── parser.py
│   ├── matcher.py
│   ├── ai_engine.py
│   └── database.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md


How to Run Locally


# Clone the repo
git clone https://github.com/YOUR_USERNAME/resume-job-assistant.git
cd resume-job-assistant

# Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run main.py


First run will download the MiniLM model (~90MB). This happens automatically.

How It Works
Upload a resume PDF → text is extracted with pdfplumber
Skills section is detected → merged with full resume scan
Paste JD → skills are extracted from a master list
Skills are converted to embeddings using the MiniLM transformer model
Cosine similarity is computed → skills matched by meaning
Fit score = semantically matched / total JD skills × 100
Gaps, tips, and questions are generated dynamically
Every analysis is auto-saved to SQLite