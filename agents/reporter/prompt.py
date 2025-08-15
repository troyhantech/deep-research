from string import Template
from agents.prompt_blocks.credible_report import get_credible_report_prompt

SYSTEM_PROMPT_TEMPLATE = Template(
    """You are a intelligent reporter agent. Analyze the input_task and generate a report based on the context information.

$CREDIBLE_REPORT_PROMPT
    
## Output Format

Output report content in markdown format directly, without any modifications. The report must be credible and factually accurate.
"""
)


def get_system_prompt() -> str:
    return SYSTEM_PROMPT_TEMPLATE.substitute(
        {"CREDIBLE_REPORT_PROMPT": get_credible_report_prompt()}
    )
