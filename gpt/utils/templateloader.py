from typing import (List, Dict, Union)


class PromptTemplate:
    def __init__(self):
        ...

    @staticmethod
    def create_few_shot_prompt(examples: Dict[str, str], new_input: str) -> str:
        _prompt: str = ""
        for example in examples:
            _prompt += f"Q: {example['input']}\nA: {example['output']}\n\n"
        _prompt += f"Q: {new_input}\nA: "
        return _prompt

    @staticmethod
    def message_loader(system_msg: str, **kwargs) -> List[Dict[str, str]]:
        rst = [{"role": "system", "content" : system_msg}]
        for k, v in kwargs.items():
            rst.append({"role": k, "content": v })
        return rst

