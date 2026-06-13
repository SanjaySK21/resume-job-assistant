# main.py

import streamlit as st
from app.parser import extract_text, extract_skills
from app.matcher import extract_jd_skills, calculate_fit_score
from app.ai_engine import generate_tips, generate_questions
from app.database import init_db, save_analysis

# ─────────────────────────────────────────
# Init DB on startup
# ─────────────────────────────────────────

init_db()

# ─────────────────────────────────────────
# Page config
# ─────────────────────────────────────────

st.set_page_config(
    page_title="Resume Job Assistant",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Resume Job Assistant")
st.caption("Upload your resume + paste a job description to get your fit score")
st.divider()

# ─────────────────────────────────────────
# STEP 1 — Resume upload
# ─────────────────────────────────────────

st.markdown("### Step 1 — Upload Resume")

uploaded_file = st.file_uploader(
    "Upload your resume (PDF only)",
    type=["pdf"]
)

resume_skills = []
raw_text = ""

if uploaded_file is not None:

    with st.spinner("Reading your resume..."):
        raw_text = extract_text(uploaded_file)

    if not raw_text:
        st.error("Could not extract text. Make sure the PDF is not scanned or image-based.")
        st.stop()

    with st.expander("View extracted resume text"):
        st.text_area("Raw text", raw_text, height=200)

    with st.spinner("Extracting skills from resume..."):
        resume_skills, method = extract_skills(raw_text)

    if method == "section":
        st.success(f"Skills extracted from Skills section — {len(resume_skills)} found")
    else:
        st.warning(f"Fallback keyword scan used — {len(resume_skills)} skills found")

    if resume_skills:
        with st.expander("View resume skills"):
            cols = st.columns(3)
            for i, skill in enumerate(resume_skills):
                cols[i % 3].write(f"✓ {skill}")
    else:
        st.error("No skills found in resume.")
        st.stop()

# ─────────────────────────────────────────
# STEP 2 — JD input
# ─────────────────────────────────────────

st.divider()
st.markdown("### Step 2 — Paste Job Description")

jd_text = st.text_area(
    "Paste the full job description here",
    height=200,
    placeholder="Example: We are looking for a Python developer with React, MySQL, and AWS experience..."
)

if uploaded_file is not None and jd_text.strip():

    if not resume_skills:
        st.error("No resume skills found. Cannot calculate fit score.")
        st.stop()

    with st.spinner("Analysing job description..."):
        jd_skills = extract_jd_skills(jd_text)
        score, matched, missing = calculate_fit_score(resume_skills, jd_skills)
        tips = generate_tips(score, missing)
        questions = generate_questions(matched, missing, score)

    # Save to DB
    save_analysis(
        resume_name=uploaded_file.name,
        fit_score=score,
        matched=matched,
        missing=missing,
        tips=tips,
        questions=questions
    )

    st.divider()
    st.markdown("### Results")

    # ── Fit score ───────────────────────────────
    st.markdown("#### Fit Score")

    if score >= 70:
        st.success(f"Fit Score: {score}%")
    elif score >= 40:
        st.warning(f"Fit Score: {score}%")
    else:
        st.error(f"Fit Score: {score}%")

    st.progress(int(score) / 100)

    col1, col2, col3 = st.columns(3)
    col1.metric("JD Skills", len(jd_skills))
    col2.metric("Matched", len(matched))
    col3.metric("Missing", len(missing))

    st.divider()

    # ── JD skills ───────────────────────────────
    st.markdown("#### Skills Detected in JD")
    if jd_skills:
        cols = st.columns(3)
        for i, skill in enumerate(jd_skills):
            cols[i % 3].write(f"• {skill}")
    else:
        st.warning("No recognizable skills found in JD.")

    st.divider()

    # ── Matched ─────────────────────────────────
    st.markdown("#### Matched Skills")
    st.caption("Skills present in both resume and JD")
    if matched:
        cols = st.columns(3)
        for i, skill in enumerate(matched):
            cols[i % 3].write(f"✅ {skill}")
    else:
        st.warning("No matching skills found.")

    st.divider()

    # ── Skill gaps ──────────────────────────────
    st.markdown("#### Skill Gaps")
    st.caption("Skills required in JD but missing from your resume")
    if missing:
        cols = st.columns(3)
        for i, skill in enumerate(missing):
            cols[i % 3].write(f"❌ {skill}")
    else:
        st.success("No skill gaps — you match all JD requirements.")

    st.divider()

    # ── Resume tips ─────────────────────────────
    st.markdown("#### Resume Tips")
    for tip in tips.split("\n\n"):
        st.info(tip)

    st.divider()

    # ── Interview questions ──────────────────────
    st.markdown("#### Interview Questions")
    st.caption("Based on your matched skills and job requirements")
    for i, q in enumerate(questions, 1):
        st.write(f"**Q{i}.** {q}")

    st.divider()
    st.caption("✅ This analysis has been saved to history.")

elif uploaded_file is not None and not jd_text.strip():
    st.info("Paste a job description above to see your fit score.")

elif uploaded_file is None:
    st.info("Upload your resume first.")