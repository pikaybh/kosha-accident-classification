import pandas as pd
import os
from typing import List
import logging

# Root 
logger_name = "utils.myos"
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

class File:
    def __init__(self):
        ...

    @staticmethod
    def readfile(file_path : str) -> pd.DataFrame:
        file_name, ext = os.path.splitext(file_path)
        extalias = ext.replace('.', '')
        if extalias == "xlsx":
            df : pd.DataFrame = pd.read_excel(file_path)
        elif extalias == "csv":
            df : pd.DataFrame = pd.read_csv(file_name, encoding="utf-8-sig")
        else:
            raise logger.Error(f"Extension `{ext}` is not supported.")
        return df

    @staticmethod
    def get_xlsx(root_dir : str) -> List[str]:
        return [file for file in os.listdir(root_dir) if "xlsx" in os.path.splitext(file)[-1]]


class MyStr(str):
    def __mul__(self, other) -> str:
        return self.split(other)[0]
