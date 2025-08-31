from openai import AsyncOpenAI
from langsmith.wrappers import wrap_openai
import os

async_openai_sdk_client = wrap_openai(
    AsyncOpenAI(max_retries=os.getenv("OPENAI_MAX_RETRIES", 3))
)
