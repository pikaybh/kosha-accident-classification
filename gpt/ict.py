# Internal Modules
from _openai import call_openai_api
from utils.templateloader import PromptTemplate
# External Modules
import logging

# Root 
logger_name = "gpt.ict"
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


def run() -> None:
    while True:
        # 새로운 질문
        new_question = "새로운 질문 내용"
        # few-shot learning prompt 생성
        prompt = create_few_shot_prompt(examples, new_question)
        # OpenAI API를 호출하여 예측 수행
        predicted_answer = call_openai_api(prompt)
        print(f"Q: {new_question}\nA: {predicted_answer}")
        