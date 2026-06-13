#parser.py

import pdfplumber
import re

# ─────────────────────────────────────────
# Section heading patterns
# ─────────────────────────────────────────

SKILLS_HEADINGS = [
    "skills summary", "technical skills", "skill summary",
    "skills", "core skills", "key skills", "technologies",
    "technical expertise", "core competencies", "skill set",
    "programming skills", "technical competencies", "tech stack",
    "areas of expertise", "tools and technologies"
]

# "languages" removed — it often appears inside skills section
STOP_HEADINGS = [
    "experience", "education", "projects", "achievements",
    "certifications", "awards", "interests", "summary",
    "objective", "about", "work experience", "internship",
    "publications", "hobbies", "volunteer"
]

# ─────────────────────────────────────────
# Fallback list — used ONLY if Skills section not found
# ─────────────────────────────────────────

FALLBACK_SKILLS = [
    "python", "java", "javascript", "typescript", "sql",
    "html", "css", "php", "kotlin", "swift", "scala",
    "react", "django", "flask", "fastapi", "spring",
    "angular", "vue", "nextjs", "nestjs", "graphql",
    "mysql", "postgresql", "sqlite", "mongodb", "redis", "firebase",
    "aws", "azure", "gcp", "linux", "microservices",
    "airflow", "spark", "kafka", "hadoop", "power bi", "tableau",
    "tensorflow", "pytorch", "pandas", "numpy", "scikit-learn",
    "machine learning", "deep learning", "nlp", "computer vision",
    "playwright", "selenium", "pytest", "jest",
    "figma", "postman", "jira", "jenkins",
    "ci/cd", "rest api", "node.js", "express.js", "react.js",
    "c++", "c/c++"
]

# ─────────────────────────────────────────
# Step 1 — Extract raw text from PDF
# ─────────────────────────────────────────

def extract_text(pdf_file):
    """
    Opens PDF, reads every page, returns full clean text as one string.
    """
    full_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    return full_text.strip()


# ─────────────────────────────────────────
# Step 2 — Detect and extract Skills section
# ─────────────────────────────────────────

def extract_skills_section(text):
    """
    Scans resume line by line.
    Finds where Skills section starts.
    Stops at next known section heading.
    Returns raw skills section text, or None if not found.
    """
    lines = text.split("\n")
    inside_skills = False
    skills_lines = []

    for line in lines:
        line_clean = line.strip()
        line_lower = line_clean.lower()

        if not inside_skills:
            for heading in SKILLS_HEADINGS:
                if line_lower == heading or line_lower.startswith(heading + ":"):
                    inside_skills = True
                    # Skills on same line as heading
                    # Example: "Skills: Python, Java, SQL"
                    if ":" in line_clean:
                        inline = line_clean.split(":", 1)[1].strip()
                        if inline:
                            skills_lines.append(inline)
                    break

        elif inside_skills:
            # Stop if we hit a new section heading
            is_stop = False
            for stop in STOP_HEADINGS:
                if line_lower == stop or line_lower.startswith(stop + ":"):
                    is_stop = True
                    break

            if is_stop:
                break

            # Safety stop — long lines are likely sentences, not skills
            if len(line_clean) > 200:
                break

            if line_clean:
                skills_lines.append(line_clean)

    if skills_lines:
        return "\n".join(skills_lines)

    return None


# ─────────────────────────────────────────
# Step 3 — Split and clean skills text
# ─────────────────────────────────────────

PROTECTED_SKILLS = [
    "ci/cd", "c/c++", "asp.net", "node.js", "express.js",
    "react.js", "vue.js", "next.js", "nest.js", ".net",
    "go/golang", "ml/ai", "ios/android"
]

def clean_and_split(skills_text):
    """
    Takes raw skills section text.
    Protects known compound skills before splitting.
    Splits by commas, bullets, pipes, newlines only.
    Returns unique list of skills in original order.
    """
    cleaned = skills_text

    # Step 1 — Protect compound skills with placeholders
    placeholders = {}
    for i, skill in enumerate(PROTECTED_SKILLS):
        placeholder = f"__SKILL{i}__"
        placeholders[placeholder] = skill
        cleaned = cleaned.replace(skill, placeholder)
        cleaned = cleaned.replace(skill.upper(), placeholder)
        cleaned = cleaned.replace(skill.title(), placeholder)

    # Step 2 — Replace safe separators
    cleaned = cleaned.replace("•", ",")
    cleaned = cleaned.replace("◦", ",")
    cleaned = cleaned.replace("|", ",")
    cleaned = cleaned.replace("\n", ",")

    # Step 3 — Split by comma
    raw_items = cleaned.split(",")

    skills = []
    for item in raw_items:
        item = item.strip()

        # Remove label prefixes like "Languages:", "Tools:", "Frameworks:"
        if ":" in item:
            item = item.split(":", 1)[1].strip()

        # Restore protected skills from placeholders
        for placeholder, original in placeholders.items():
            item = item.replace(placeholder, original)

        # Remove leftover bullet characters and trailing punctuation
        item = item.lstrip("•◦-– ").strip()
        item = item.strip(".,;:")  # fix: removes trailing period like "AWS."

        # Skip empty, too short, or sentence-length items
        if 1 <= len(item) <= 40:
            skills.append(item)

    # Remove duplicates — keep original order (no sorted())
    seen = set()
    unique_skills = []
    for s in skills:
        key = s.lower()
        if key not in seen:
            seen.add(key)
            unique_skills.append(s)

    return unique_skills


# ─────────────────────────────────────────
# Step 4 — Fallback keyword matching
# ─────────────────────────────────────────

def fallback_extraction(text):
    """
    Used ONLY when Skills section not found.
    Uses word boundary matching to avoid false matches.
    c++ handled separately because \\b breaks on + symbol.
    """
    matched = []

    for skill in FALLBACK_SKILLS:
        # c++ and c/c++ — word boundary doesn't work, use substring
        if skill in ["c++", "c/c++"]:
            if skill.lower() in text.lower():
                matched.append(skill)

        # Short skills (2–3 chars) like sql, php — use word boundary
        elif len(skill) <= 3:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                matched.append(skill)

        # Longer skills — substring match is safe enough
        else:
            if skill.lower() in text.lower():
                matched.append(skill)

    return matched


# ─────────────────────────────────────────
# Main function — called from main.py
# ─────────────────────────────────────────

# def extract_skills(text):
#     """
#     Hybrid flow:
#     1. Try section-based extraction first
#     2. If found and has results → return those
#     3. If not found → fallback to keyword scan
#     Returns (skills_list, method_used)
#     """
#     skills_section = extract_skills_section(text)

#     if skills_section:
#         skills = clean_and_split(skills_section)
#         if skills:
#             return skills, "section"

#     # Fallback
#     skills = fallback_extraction(text)
#     return skills, "fallback"


def extract_skills(text):
    """
    Hybrid flow:
    1. Try section-based extraction first
    2. Also scan full resume text for additional skills
    3. Merge both results
    Returns (skills_list, method_used)
    """
    section_skills = []
    method = "fallback"

    skills_section = extract_skills_section(text)
    if skills_section:
        section_skills = clean_and_split(skills_section)
        if section_skills:
            method = "section"

    # Always also run fallback on full text to catch skills in experience/projects
    full_text_skills = fallback_extraction(text)

    # Merge both — section skills first, then add any extras from full text
    seen = set()
    merged = []

    for s in section_skills:
        key = s.lower()
        if key not in seen:
            seen.add(key)
            merged.append(s)

    for s in full_text_skills:
        key = s.lower()
        if key not in seen:
            seen.add(key)
            merged.append(s)

    if merged:
        return merged, method

    return [], "fallback"