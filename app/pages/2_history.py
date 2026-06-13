# app/pages/2_history.py

import streamlit as st
from app.database import get_all_analyses

st.set_page_config(
    page_title="Analysis History",
    page_icon="🕓",
    layout="centered"
)

st.title("🕓 Analysis History")
st.caption("All past resume analyses saved to database")
st.divider()

analyses = get_all_analyses()

if not analyses:
    st.info("No analyses saved yet. Go to the main page and analyse a resume first.")
    st.stop()

st.write(f"Total analyses saved: **{len(analyses)}**")
st.divider()

for record in analyses:
    with st.expander(
        f"#{record['id']} — {record['resume_name']} | "
        f"Score: {record['fit_score']}% | {record['timestamp']}"
    ):
        if record['fit_score'] >= 70:
            st.success(f"Fit Score: {record['fit_score']}%")
        elif record['fit_score'] >= 40:
            st.warning(f"Fit Score: {record['fit_score']}%")
        else:
            st.error(f"Fit Score: {record['fit_score']}%")

        st.progress(int(record['fit_score']) / 100)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Matched Skills**")
            if record['matched']:
                for s in record['matched']:
                    st.write(f"✅ {s}")
            else:
                st.write("None")

        with col2:
            st.markdown("**Skill Gaps**")
            if record['missing']:
                for s in record['missing']:
                    st.write(f"❌ {s}")
            else:
                st.write("None")

        st.divider()
        st.markdown("**Resume Tips**")
        for tip in record['tips'].split("\n\n"):
            st.info(tip)

        st.markdown("**Interview Questions**")
        for i, q in enumerate(record['questions'], 1):
            st.write(f"**Q{i}.** {q}")