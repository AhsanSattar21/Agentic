import os
import streamlit as st
from research_agent import run_research

st.set_page_config(page_title="AI Research Agent", page_icon="🔎")
st.title("🔎 AI Research Agent")
st.caption("CrewAI + Groq (gpt-oss-120b) + DuckDuckGo")

# Get API key: Streamlit secrets (cloud) or environment variable (local)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found. Add it to Streamlit secrets (see README).")
    st.stop()

topic = st.text_input("Enter a research topic:", placeholder="e.g. Future of solid-state batteries")

if st.button("Generate Report", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Researching... this can take 1-2 minutes ⏳"):
            try:
                report = run_research(topic.strip(), api_key)
                st.markdown(report)
                st.download_button(
                    "Download report (.md)",
                    data=report,
                    file_name="research_report.md",
                    mime="text/markdown",
                )
            except Exception as e:
                st.error(f"Something went wrong: {e}")
