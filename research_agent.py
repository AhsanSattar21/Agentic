import os

# Turn off telemetry (faster startup, fewer warnings on cloud)
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from ddgs import DDGS


# ---------- 1. Free search tool (DuckDuckGo) ----------
@tool("Web Search")
def web_search(query: str) -> str:
    """Search the web with DuckDuckGo. Input is a search query string.
    Returns titles, links and short snippets of the top results."""
    try:
        results = DDGS().text(query, max_results=5)
    except Exception as e:
        return f"Search failed: {e}"

    if not results:
        return "No results found."

    lines = []
    for r in results:
        lines.append(f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n")
    return "\n".join(lines)


# ---------- 2. Build the crew and run it ----------
def run_research(topic: str, api_key: str) -> str:
    llm = LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=api_key,
        temperature=0.3,
        max_tokens=4000,
    )

    researcher = Agent(
        role="Senior Research Analyst",
        goal=f"Research '{topic}' thoroughly and write an accurate, well-structured report.",
        backstory=(
            "You are an experienced analyst. You search the web, compare sources, "
            "and only state facts that you found in the search results."
        ),
        tools=[web_search],
        llm=llm,
        max_iter=8,        # limits how many thinking/search loops it can do
        verbose=False,
    )

    task = Task(
        description=(
            f"Research the topic: '{topic}'.\n"
            "Use the Web Search tool 3-5 times with different queries. "
            "Then write a report based on what you found."
        ),
        expected_output=(
            "A markdown report with these sections: Title, Introduction, "
            "Key Findings (bullet points), Detailed Analysis, Conclusion, "
            "and Sources (list of URLs used)."
        ),
        agent=researcher,
    )

    crew = Crew(
        agents=[researcher],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()
    return result.raw
