# ai_engine.py

# ─────────────────────────────────────────
# Rule-based AI outputs — fully dynamic
# Works for any skill — no hardcoded skill list
# ─────────────────────────────────────────

def generate_tips(fit_score, missing_skills):
    """
    Generates resume tips based on fit score and missing skills.
    Fully dynamic — works on any score and any missing skill list.
    """
    tips = []

    if fit_score == 100:
        tips.append(
            "Excellent match. Your resume covers all required skills. "
            "Focus on quantifying your achievements with numbers and impact."
        )
    elif fit_score >= 70:
        tips.append(
            "Strong match. You meet most requirements. "
            "Highlight your matching skills at the top of your resume "
            "to pass ATS screening quickly."
        )
    elif fit_score >= 40:
        tips.append(
            "Moderate match. You have relevant skills but gaps exist. "
            "Consider adding projects or certifications "
            "to show you are actively learning the missing skills."
        )
    else:
        tips.append(
            "Low match. This role requires skills you have not listed yet. "
            "Focus on building 1-2 of the missing skills through a small project "
            "before applying."
        )

    # Dynamic tip — built from actual missing skills, not hardcoded
    if missing_skills:
        top_missing = missing_skills[:3]
        skills_str = ", ".join(top_missing)
        tips.append(
            f"Priority skills to add: {skills_str}. "
            f"Even a small personal project using these will strengthen your profile."
        )

    tips.append(
        "Make sure your Skills section is clearly labeled and near the top. "
        "Many ATS systems scan the top third of your resume first."
    )

    return "\n\n".join(tips)


# ─────────────────────────────────────────
# Dynamic question templates
# Applied to ANY skill — no skill name hardcoded
# ─────────────────────────────────────────

# These are generic templates with {skill} placeholder
# Works for React, Go, Figma, Terraform — anything
QUESTION_TEMPLATES = [
    "Can you describe a project where you used {skill}? What problem did it solve?",
    "What are the key features of {skill} that make it useful in real projects?",
    "How did you learn {skill} and how have you applied it professionally?",
    "What challenges have you faced while working with {skill} and how did you overcome them?",
    "How does {skill} compare to similar tools or technologies you have used?",
]

GAP_TEMPLATE = (
    "You do not have {skill} listed on your resume. "
    "Are you familiar with it? How quickly could you learn it?"
)


def generate_questions(matched_skills, missing_skills, fit_score):
    """
    Generates interview questions dynamically.
    Uses templates with {skill} placeholder — works for ANY skill.
    No hardcoded skill names or hardcoded questions.

    Logic:
    - Pick up to 4 matched skills
    - For each, rotate through question templates
    - Add 1 gap question from missing skills
    - Add 2 generic behavioural questions always
    """
    questions = []

    # Pick top matched skills — max 4 to keep output focused
    top_matched = matched_skills[:4]

    for i, skill in enumerate(top_matched):
        # Rotate through templates — each skill gets a different template
        template = QUESTION_TEMPLATES[i % len(QUESTION_TEMPLATES)]
        question = template.replace("{skill}", skill)
        questions.append(question)

    # Add one gap awareness question from missing skills
    if missing_skills:
        gap_skill = missing_skills[0]
        questions.append(GAP_TEMPLATE.replace("{skill}", gap_skill))

    # Generic behavioural questions — always added, not skill specific
    questions.append(
        "Tell me about a technical challenge you faced in a project "
        "and how you solved it."
    )
    questions.append(
        "How do you stay updated with new technologies in your field?"
    )

    return questions