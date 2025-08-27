from agents.planner.agent import create_agent
from config import CONFIG


UNLIMITED_RECURSION_LIMIT = 1000


async def deep_research(task: str) -> str:
    """Deep research the topic task"""
    agent = create_agent()
    result = await agent.ainvoke(
        {
            "task": task,
            "remaining_reasoning_times": CONFIG.get("agents", {})
            .get("planner", {})
            .get("max_reasoning_times", 10),
        },
        config={
            "recursion_limit": UNLIMITED_RECURSION_LIMIT,
        },
    )
    return result["result"]
