import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Internal Modules
from config.api_keys import openai_api_key
# External Modules
import openai
from typing import (List, Dict, Union)
import logging

# Root 
logger_name = 'gpt._openai'
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)
# File Handler
file_handler = logging.FileHandler(f'logs/{logger_name}.log', encoding='utf-8-sig')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(r'%(asctime)s [%(name)s, line %(lineno)d] %(levelname)s: %(message)s'))
logger.addHandler(file_handler)
# Stream Handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(r'%(message)s'))
logger.addHandler(stream_handler)

# 모델을 호출하는 함수입니다.
def call_openai_api(messages : List[Dict[str, Union[str, List[Dict[str, str]]]]], model : str = "gpt-4o", temperature : float = .5, max_tokens : int = 150, top_p : float = 1., frequency_penalty : float = .0, presence_penalty : float = .0) -> str:
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=messages,  # "text-davinci-003"
        temperature=temperature, 
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    return response.choices[0].message.content
"""
def call_assistant_api(name="Financial Analyst Assistant",
instructions="You are an expert financial analyst. Use you knowledge base to answer questions about audited financial statements.",
model="gpt-4o",
tools=[{"type": "file_search"}]) -> openai.Any:
    _assitant : openai.OpenAI.beta.assistants = openai.OpenAI.beta.assistants.create(
        name=name,
        instructions=instructions,
        model=model,
        tools=tools
    )
    return _assitant
"""