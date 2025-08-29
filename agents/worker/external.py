from agents.worker.agent import create_agent
import asyncio


async def call_worker(task: str, config: dict) -> str:
    """
    Call worker to execute subtask.

    Return the result of worker.
    """

    worker_agent = await create_agent()
    result = await worker_agent.ainvoke(
        {
            "task": task,
            "config": config,
        }
    )
    return result["result"]


async def call_workers(tasks: list[str], config: dict) -> str:
    """
    Call workers to execute subtasks in parallel.

    Return the aggregated result of workers.
    """
    workers_result = await asyncio.gather(
        *[call_worker(task, config) for task in tasks]
    )
    return "\n====\n".join(workers_result)
