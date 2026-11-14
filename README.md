# AI Research Agent

Single-agent research app built with CrewAI, Groq (`openai/gpt-oss-120b`), DuckDuckGo search and Streamlit.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export GROQ_API_KEY="your_key" # Windows PowerShell: $env:GROQ_API_KEY="your_key"
streamlit run app.py
```

## Deploy on Streamlit Cloud
1. Push this repo to GitHub.
2. On share.streamlit.io create an app, main file `app.py`.
3. Advanced settings: Python version **3.12**.
4. Secrets:
   ```toml
   GROQ_API_KEY = "your_real_key"
   ```
