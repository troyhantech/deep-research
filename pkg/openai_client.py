from openai import AsyncOpenAI
from langsmith.wrappers import wrap_openai
import os

_async_openai_sdk_client = None


def get_async_openai_client():
    global _async_openai_sdk_client
    if _async_openai_sdk_client is None:
        init_openai_client()
    return _async_openai_sdk_client


def init_openai_client():
    global _async_openai_sdk_client
    _async_openai_sdk_client = wrap_openai(
        AsyncOpenAI(max_retries=int(os.getenv("OPENAI_MAX_RETRIES", "3")))
    )
