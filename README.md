# Semantic Resume Job Assistant

A GenAI-powered resume analyzer built with **Python** and **Streamlit**.

Upload a resume PDF and paste a job description to get:

- Semantic fit score
- Skill gap analysis
- Resume tips
- Interview questions

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit |
| PDF Parsing | pdfplumber |
| Skill Extraction | LLM-based dynamic extraction (Groq Llama-3) + section parser |
| Matching | Semantic embeddings (MiniLM) + cosine similarity |
| Embedding Model | sentence-transformers (all-MiniLM-L6-v2) |
| LLM | Groq API (llama-3.1-8b-instant) |
| AI Outputs | Rule-based dynamic templates |
| Database | SQLite |
| Language | Python 3 |

---

## What Makes It GenAI

This project combines **two GenAI techniques**:

### 1. LLM-Based Skill Extraction

Instead of using a hardcoded skill list, an LLM (Groq Llama-3) reads the entire resume and job description to extract skills dynamically, including skills described inside sentences.

**Example:**

> "Fine-tuned a DistilBERT model"

Extracted skill:

> Fine-tuning

### 2. Semantic Embedding Matching

A transformer model (MiniLM) converts skills into vector embeddings and compares them based on **meaning**, not exact text.

| Scenario | Old (String Match) | New (Semantic Match) |
|----------|---------------------|----------------------|
| ML vs Machine Learning | ❌ Miss | ✅ Match |
| NodeJS vs node | ❌ Miss | ✅ Match |
| REST APIs vs rest api | ❌ Miss | ✅ Match |
| RAG pipeline (mentioned inside a sentence) | ❌ Miss | ✅ Extracted by LLM |

A safety filter verifies that every LLM-extracted skill actually appears in the source text, preventing hallucinated skills from affecting results.

---

## Project Structure

```text
resume-job-assistant/
│
├── app/
│   ├── .streamlit/
│   │   └── config.toml
│   ├── pages/
│   │   └── 2_history.py
│   ├── parser.py
│   ├── matcher.py
│   ├── ai_engine.py
│   └── database.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## How to Run Locally

```bash
# Clone the repository
git clone https://github.com/SanjaySK21/resume-job-assistant.git

# Move into the project folder
cd resume-job-assistant

# Create a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file
GROQ_API_KEY=your_key_here

# Run the application
streamlit run main.py
```

> **Note:** The first run automatically downloads the MiniLM embedding model (~90 MB).

---

## How It Works

1. Upload a resume PDF → Text extracted using **pdfplumber**
2. Resume skills section detected and merged with LLM extraction
3. Paste a Job Description
4. LLM extracts skills dynamically (no hardcoded skill list)
5. Safety filter validates extracted skills against the original text
6. Skills are converted into MiniLM embeddings
7. Cosine similarity performs semantic skill matching
8. Fit Score = Matched JD Skills ÷ Total JD Skills × 100
9. Resume tips, missing skills, and interview questions are generated
10. Every analysis is automatically stored in SQLite