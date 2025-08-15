from config import CONFIG
from pkg.openai_client import async_openai_sdk_client
from agents.reporter.prompt import get_system_prompt


async def generate_report(info: str, input_task: str) -> str:
    system_prompt = get_system_prompt()

    user_content = f"""
    <input_task>
    {input_task}
    </input_task>

    Please generate a report based on the following information:
    {info}
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]

    response = await async_openai_sdk_client.chat.completions.create(
        model=CONFIG["agents"]["reporter"]["model"],
        messages=messages,
        max_tokens=CONFIG["agents"]["reporter"]["max_tokens"],
    )

    return response.choices[0].message.content
