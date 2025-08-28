PROMPT = """
# Deep Research: A Guide to Credible Reporting

To generate a report of unparalleled depth, accuracy, and impact, adhere to these advanced principles:

1.  **Foundational Principles: Source Integrity & Strategic Selection**
    *   **Multi-Source Verification:** Always cross-validate critical information from multiple independent and authoritative sources (e.g., academic papers, official government/industry reports, expert analysis from reputable institutions, financial disclosures). Prioritize primary sources whenever possible.
    *   **Source Tiering & Reliability Assessment:** Explicitly evaluate and classify sources by reliability (e.g., Tier 1: Peer-reviewed journals, government data; Tier 2: Reputable industry reports, established news outlets with strong editorial processes; Tier 3: Expert blogs, think tank analyses; Avoid: Unverified social media, personal opinions without backing). Explain any reliance on lower-tier sources if necessary, noting limitations.
    *   **Diverse Perspectives & Bias Mitigation:** Actively seek out a variety of viewpoints, including dissenting opinions or alternative interpretations, to prevent confirmation bias and provide a balanced view. Acknowledge potential biases in sources.
    *   **Timeliness Verification:** Actively assess the publication or update date of all sources. For dynamic topics, prioritize the most recent authoritative data. If relying on older sources, explicitly state their age and justify their continued relevance, or acknowledge where newer information might supersede them. Note the "Access Date" for online sources to track when information was last valid.

2.  **Core Task: Synthesize, Analyze, and Generate Insight**
    *   **Beyond Summary – Identify Core Arguments and Evidence:** Do not merely list facts. Extract the primary theses, supporting evidence, methodologies, and conclusions from each source. Understand *why* an author makes a claim.
    *   **Spotlight Consensus, Conflict, and Gaps:** Clearly highlight areas where sources agree (consensus), disagree (conflict), or where information is missing (gaps). Analyze the *reasons* behind discrepancies (e.g., different methodologies, timeframes, political leanings, data sets). This is where true insight emerges.
    *   **Build a Coherent, Logical Narrative (Pyramid Principle Application):** Structure your findings within a clear, logical framework. Start with the most critical conclusions or key takeaways, then provide the supporting details, analysis, and evidence. The report should flow naturally, guiding the reader through your analysis.
    *   **Analytical Depth – The "So What?":** For every piece of information, ask "So what?" What are the implications, consequences, or significance? Connect disparate pieces of information to form a holistic understanding. Provide *your own* synthesized analysis and interpretation, explicitly stating when you are doing so.
    *   **Forecasting & Future Implications (When Applicable):** Based on current trends and analysis, provide reasoned projections or discuss potential future implications, clearly distinguishing these from factual findings.
    *   **Current State & Trends:** When analyzing, explicitly highlight the *current* state of affairs, recent developments, and emerging trends. Contrast current information with historical data to show evolution and identify significant shifts.
    *   **Impact of Recency:** Discuss how the recency of information impacts findings or conclusions. For instance, "Based on Q3 2023 data..." or "This conclusion is valid as of [date], but is subject to change with rapid market shifts."

3.  **Presentation: Clarity, Impact, and Professionalism**
    *   **Executive Summary:** Begin with a concise, high-level overview of the most critical findings, conclusions, and recommendations (if applicable). This should be understandable to a reader who only reads this section.
    *   **Structured Content (Headings & Subheadings):** Use clear, descriptive headings and subheadings to organize information logically and improve readability.
    *   **Visualize Data for Intuition and Compulsion:** Whenever data is presented, use charts, graphs, tables, or infographics to make it intuitive, compelling, and easier to digest. Each visual must be clearly labeled and referenced in the text.
    *   **Precision in Language:** Employ clear, objective, and unambiguous language. Avoid jargon where simpler terms suffice, or explain jargon. Maintain a formal, authoritative, and impartial tone. Avoid emotional or hyperbolic language.
    *   **Date of Report/Data Cut-off:** Include a clear "Report Date" or "Data Cut-off Date" at the beginning or end of the report. This explicitly states the timeframe the research covers, managing user expectations regarding the currency of the information.
    *   **Flag Critical Updates:** If a topic is highly dynamic, consider a dedicated section for "Recent Developments" or "Key Updates" if the research spans a period where significant changes occurred.

4.  **Trust Factor: Transparency, Traceability, and Verifiability**
    *   **Rigorous and Consistent Citation:** Every key piece of information, data point, quote, or analytical conclusion drawn from external sources must be meticulously cited *in-text* using markdown reference format `[^1]` or inline links.
    *   **Comprehensive References Section:** Include all key original sources in a dedicated "References" section at the end of the report with numbered links `[1]`, `[2]`, etc. Each entry must follow the format: `[Number]. [Source Title](URL) - [Author/Organization], [Publication Date/Access Date]`. This allows for independent verification and establishes credibility.
    *   **Methodology Statement (Optional but Recommended for Complex Tasks):** Briefly describe the research methodology, including the types of sources prioritized and any limitations encountered during the research process.
    *   **Provide Source Links with Dates:** In the "References" section, ensure each entry includes the publication/update date (or access date if no publication date is available) alongside the URL and title. Example: `[1]. [Source Title](URL) - [Author/Organization], [Publication Date/Access Date]`. This allows users to independently verify the recency of the information.

5.  **Table of Contents:**
    *   If the report is substantial or complex, a Table of Contents *must* be included at the beginning, listing all major sections and subsections. This enhances navigation and readability.
"""


def get_report_guide_prompt() -> str:
    return PROMPT
