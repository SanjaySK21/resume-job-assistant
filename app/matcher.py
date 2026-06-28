# # # matcher.py
# # # matcher.py

# # import re

# # # ─────────────────────────────────────────
# # # Master skills list for JD keyword matching
# # # ─────────────────────────────────────────

# # MASTER_SKILLS = [
# #     "python", "java", "javascript", "typescript", "sql",
# #     "html", "css", "php", "kotlin", "swift", "scala",
# #     "c++", "go", "rust",
# #     "react", "angular", "vue", "django", "flask", "fastapi",
# #     "spring", "nextjs", "nestjs", "express", "graphql",
# #     "mysql", "postgresql", "sqlite", "mongodb", "redis", "firebase",
# #     "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
# #     "linux", "git", "github", "ci/cd", "microservices",
# #     "airflow", "spark", "kafka", "hadoop", "power bi", "tableau",
# #     "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
# #     "machine learning", "deep learning", "nlp",
# #     "playwright", "selenium", "pytest", "jest", "postman",
# #     "figma", "jira", "rest api", "jwt", "oauth", "agile", "scrum",
# #     "node", "bootstrap", "tailwind",
# # ]


# # # ─────────────────────────────────────────
# # # Normalization — algorithmic, not hardcoded map
# # # ─────────────────────────────────────────

# # def normalize_skill(skill):
# #     """
# #     Converts skill names to a common base form for comparison.
# #     This is algorithmic — strips known suffixes, lowercases.
# #     Not a hardcoded mapping.

# #     Examples:
# #         ReactJS   → react
# #         Node.js   → node
# #         ExpressJS → express
# #         TailwindCSS → tailwindcss (kept as is — no js suffix)
# #         Python    → python
# #         CI/CD     → ci/cd
# #     """
# #     s = skill.lower().strip()

# #     # Remove .js suffix — Node.js → node, Express.js → express
# #     if s.endswith('.js'):
# #         s = s[:-3]

# #     # Remove js suffix for longer words — ReactJS → react, NodeJS → node
# #     # Only if removing "js" still leaves at least 3 characters
# #     elif s.endswith('js') and len(s) > 4:
# #         s = s[:-2]

# #     return s.strip()


# # def normalize_text(text):
# #     """
# #     Normalizes skill mentions inside raw JD text before scanning.
# #     This converts ReactJS → react, Node.js → node in the text itself.
# #     Algorithmic — uses regex pattern, not a word list.

# #     Also handles the java/javascript false positive:
# #     After normalization, javascript stays as javascript.
# #     Word boundary check on 'java' then won't match inside 'javascript'.
# #     """
# #     t = text.lower()

# #     # Remove .js suffix from words — Node.js → node
# #     t = re.sub(r'\b(\w+)\.js\b', lambda m: m.group(1), t)

# #     # Remove js suffix from longer words — reactjs → react, nodejs → node
# #     # (\w{3,}) ensures at least 3 chars remain after stripping js
# #     t = re.sub(r'\b(\w{3,})js\b', lambda m: m.group(1), t)

# #     return t


# # # ─────────────────────────────────────────
# # # Step 1 — Extract skills from JD text
# # # ─────────────────────────────────────────

# # def extract_jd_skills(jd_text):
# #     """
# #     Normalizes JD text first.
# #     Then scans against MASTER_SKILLS (also normalized).
# #     Uses word boundary for ALL skills — prevents java matching inside javascript.
# #     Returns list of original skill names found.
# #     """
# #     jd_normalized = normalize_text(jd_text)

# #     found = []

# #     for skill in MASTER_SKILLS:
# #         skill_norm = normalize_skill(skill)

# #         # Word boundary on ALL skills — clean and safe
# #         # re.escape handles special chars like c++, ci/cd
# #         pattern = r'\b' + re.escape(skill_norm) + r'\b'

# #         if re.search(pattern, jd_normalized):
# #             found.append(skill)

# #     # Remove duplicates — keep order
# #     seen = set()
# #     unique = []
# #     for s in found:
# #         if s not in seen:
# #             seen.add(s)
# #             unique.append(s)

# #     return unique


# # # ─────────────────────────────────────────
# # # Step 2 — Calculate fit score
# # # ─────────────────────────────────────────

# # def calculate_fit_score(resume_skills, jd_skills):
# #     """
# #     Normalizes both resume skills and JD skills before comparing.
# #     This means ReactJS (resume) matches react (JD) correctly.

# #     Formula:
# #         fit_score = (matched / total_jd_skills) * 100

# #     Returns:
# #         score   — float 0 to 100
# #         matched — original JD skill names that matched
# #         missing — original JD skill names that did not match
# #     """
# #     if not jd_skills:
# #         return 0.0, [], []

# #     # Normalize resume skills into a set for fast lookup
# #     resume_normalized = {normalize_skill(s) for s in resume_skills}

# #     matched = []
# #     missing = []

# #     for skill in jd_skills:
# #         skill_norm = normalize_skill(skill)
# #         if skill_norm in resume_normalized:
# #             matched.append(skill)
# #         else:
# #             missing.append(skill)

# #     score = (len(matched) / len(jd_skills)) * 100

# #     return round(score, 1), matched, missing






# # matcher.py

# import re
# from sentence_transformers import SentenceTransformer, util

# # ─────────────────────────────────────────
# # Load MiniLM model once — not on every call
# # ─────────────────────────────────────────

# model = SentenceTransformer("all-MiniLM-L6-v2")

# # ─────────────────────────────────────────
# # Master skills list for JD keyword matching
# # ─────────────────────────────────────────

# MASTER_SKILLS = [
#     "python", "java", "javascript", "typescript", "sql",
#     "html", "css", "php", "kotlin", "swift", "scala",
#     "c++", "go", "rust",
#     "react", "angular", "vue", "django", "flask", "fastapi",
#     "spring", "nextjs", "nestjs", "express", "graphql",
#     "mysql", "postgresql", "sqlite", "mongodb", "redis", "firebase",
#     "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
#     "linux", "git", "github", "ci/cd", "microservices",
#     "airflow", "spark", "kafka", "hadoop", "power bi", "tableau",
#     "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
#     "machine learning", "deep learning", "nlp",
#     "playwright", "selenium", "pytest", "jest", "postman",
#     "figma", "jira", "rest api", "jwt", "oauth", "agile", "scrum",
#     "node", "bootstrap", "tailwind",
# ]

# # ─────────────────────────────────────────
# # Normalization — same as before
# # ─────────────────────────────────────────

# def normalize_skill(skill):
#     s = skill.lower().strip()
#     if s.endswith('.js'):
#         s = s[:-3]
#     elif s.endswith('js') and len(s) > 4:
#         s = s[:-2]
#     return s.strip()


# def normalize_text(text):
#     t = text.lower()
#     t = re.sub(r'\b(\w+)\.js\b', lambda m: m.group(1), t)
#     t = re.sub(r'\b(\w{3,})js\b', lambda m: m.group(1), t)
#     return t


# # ─────────────────────────────────────────
# # Step 1 — Extract skills from JD text
# # ─────────────────────────────────────────

# def extract_jd_skills(jd_text):
#     jd_normalized = normalize_text(jd_text)
#     found = []
#     for skill in MASTER_SKILLS:
#         skill_norm = normalize_skill(skill)
#         pattern = r'\b' + re.escape(skill_norm) + r'\b'
#         if re.search(pattern, jd_normalized):
#             found.append(skill)
#     seen = set()
#     unique = []
#     for s in found:
#         if s not in seen:
#             seen.add(s)
#             unique.append(s)
#     return unique


# # ─────────────────────────────────────────
# # Step 2 — Semantic fit score using embeddings
# # ─────────────────────────────────────────

# def calculate_fit_score(resume_skills, jd_skills, threshold=0.60):
#     """
#     Uses MiniLM embeddings + cosine similarity.
#     Matches skills by MEANING not exact string.
#     'ML' matches 'Machine Learning', 'NLP' matches 'Natural Language Processing'.

#     Returns:
#         score   — float 0 to 100
#         matched — JD skills that semantically matched
#         missing — JD skills that did not match
#     """
#     if not jd_skills or not resume_skills:
#         return 0.0, [], []

#     # Convert all skills to embeddings
#     resume_embeddings = model.encode(resume_skills, convert_to_tensor=True)
#     jd_embeddings = model.encode(jd_skills, convert_to_tensor=True)

#     matched = []
#     missing = []

#     for i, jd_skill in enumerate(jd_skills):
#         # Compare this JD skill against ALL resume skills
#         scores = util.cos_sim(jd_embeddings[i], resume_embeddings)[0]
#         best_score = scores.max().item()

#         if best_score >= threshold:
#             matched.append(jd_skill)
#         else:
#             missing.append(jd_skill)

#     score = round((len(matched) / len(jd_skills)) * 100, 1)
#     return score, matched, missing






























# matcher.py

import re
import os
import json
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer, util

load_dotenv()

# ─────────────────────────────────────────
# Load models once
# ─────────────────────────────────────────

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ─────────────────────────────────────────
# Normalization helpers — still useful
# ─────────────────────────────────────────

def normalize_skill(skill):
    s = skill.lower().strip()
    if s.endswith('.js'):
        s = s[:-3]
    elif s.endswith('js') and len(s) > 4:
        s = s[:-2]
    return s.strip()


# ─────────────────────────────────────────
# Step 1 — Extract JD skills using LLM (dynamic, no hardcoded list)
# ─────────────────────────────────────────

def extract_jd_skills(jd_text):
    """
    Uses Groq LLM to dynamically extract ALL technical skills,
    tools, and technologies from JD text.
    Works for ANY skill — Google Vision API, RBAC, Node-Cron, etc.
    No hardcoded list.
    """
    prompt = f"""Extract all technical skills, tools, frameworks, and technologies mentioned in this job description.

Job Description:
{jd_text}

Return ONLY a JSON array of skill names, nothing else. No explanation, no markdown.
Example format: ["Python", "React", "AWS"]
"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        raw = response.choices[0].message.content.strip()

        # Clean markdown fences if present
        raw = raw.replace("```json", "").replace("```", "").strip()

        skills = json.loads(raw)

        # Remove duplicates, keep order
        seen = set()
        unique = []
        for s in skills:
            key = s.lower()
            if key not in seen:
                seen.add(key)
                unique.append(s)

        return unique

    except Exception as e:
        print(f"LLM extraction failed: {e}")
        return []


# ─────────────────────────────────────────
# Step 2 — Semantic fit score using embeddings (unchanged)
# ─────────────────────────────────────────

def calculate_fit_score(resume_skills, jd_skills, threshold=0.60):
    """
    Uses MiniLM embeddings + cosine similarity.
    Matches skills by MEANING not exact string.
    """
    if not jd_skills or not resume_skills:
        return 0.0, [], []

    resume_embeddings = embed_model.encode(resume_skills, convert_to_tensor=True)
    jd_embeddings = embed_model.encode(jd_skills, convert_to_tensor=True)

    matched = []
    missing = []

    for i, jd_skill in enumerate(jd_skills):
        scores = util.cos_sim(jd_embeddings[i], resume_embeddings)[0]
        best_score = scores.max().item()

        if best_score >= threshold:
            matched.append(jd_skill)
        else:
            missing.append(jd_skill)

    score = round((len(matched) / len(jd_skills)) * 100, 1)
    return score, matched, missing