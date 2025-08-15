from agents.planner.agent import create_agent
from config import CONFIG


async def deep_research(task: str) -> str:
    """Deep research the topic task"""
    agent = create_agent()
    result = await agent.ainvoke(
        {
            "task": task,
            "remaining_reasoning_times": CONFIG.get("agents", {})
            .get("planner", {})
            .get("max_reasoning_times", 10),
        }
    )
    return result["result"]
