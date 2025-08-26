from agents.worker.agent import create_agent
import asyncio
from config import CONFIG


async def call_worker(task: str) -> str:
    """
    Call worker to execute subtask.

    Return the result of worker.
    """

    agent = await create_agent()
    result = await agent.ainvoke(
        {
            "task": task,
            "remaining_reasoning_times": CONFIG.get("agents", {})
            .get("worker", {})
            .get("max_reasoning_times", 10),
        }
    )
    return result["result"]


async def call_workers(tasks: list[str]) -> str:
    """
    Call workers to execute subtasks in parallel.

    Return the aggregated result of workers.
    """
    workers_result = await asyncio.gather(*[call_worker(task) for task in tasks])
    return "\n\n".join(workers_result)
