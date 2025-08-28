from openai import AsyncOpenAI
from langsmith.wrappers import wrap_openai
import os
from config import OPENAI_MAX_RETRIES

async_openai_sdk_client = wrap_openai(AsyncOpenAI(max_retries=OPENAI_MAX_RETRIES))
