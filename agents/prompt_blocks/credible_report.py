PROMPT = """
## Deep Research: A Guide to Credible Reporting

1. Foundational Principles: Source Integrity
  Multi-Source Verification: Always cross-validate critical information from multiple independent and authoritative sources (e.g., academic papers, official reports, expert analysis).
  Source Tiering: Classify sources by reliability. Prioritize information from top-tier sources over less credible ones like unverified blogs or social media.
  Diverse Perspectives: Actively seek out a variety of viewpoints to prevent bias and escape information bubbles.
2. Core Task: Synthesize, Don't Just Summarize
  Identify Core Arguments: Move beyond simple data collection. Extract the primary theses, supporting evidence, and conclusions from each source.
  Spotlight Consensus & Conflict: Highlight areas where sources agree, disagree, or present conflicting information. Analyze the reasons behind these discrepancies.
  Build a Logical Narrative: Structure your findings within a clear, logical framework (e.g., Introduction -> Core Findings -> Analysis -> Conclusion). Don't just list facts.
3. Presentation: Clarity and Impact
  Pyramid Principle: Start with the most critical conclusion, then provide the supporting details. This ensures your key message is delivered effectively.
  Visualize Data: Use charts and graphs to make data intuitive and compelling. Visuals are more powerful than raw numbers.
  Precision in Language: Employ clear, objective, and unambiguous language. Avoid jargon and emotionally charged terms.
4. Trust Factor: Transparency and Traceability
  Rigorous Citation: Every key piece of information, data point, or quote must be meticulously cited using markdown reference format [^1] or inline links.
  Provide Source Links: Include all key original sources in a "References" section at the end of the report with numbered links [1], [2], etc., allowing for independent verification. Use markdown link format: [Source Title](URL).
5. Table of Contents:
  If you determine that including a table will help illustrate, organize, or enhance the information in the research output, you must explicitly provide them.
"""


def get_credible_report_prompt() -> str:
    return PROMPT
