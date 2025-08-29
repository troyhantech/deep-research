from agents.planner.agent import create_agent


UNLIMITED_RECURSION_LIMIT = 1000


async def deep_research(task: str, config: dict) -> str:
    """Deep research the topic task"""
    planner_agent = create_agent()

    input = {
        "task": task,
        "config": config,
    }
    result = await planner_agent.ainvoke(
        input,
        config={
            "recursion_limit": UNLIMITED_RECURSION_LIMIT,
        },
    )
    return result["result"]
