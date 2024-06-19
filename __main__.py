# Internal Modules
from config.api_keys import openai_api_key
from utils.myos import File
from gpt.zsl import classify_case
# External Modules
# from functools import lru_cache
from tqdm import tqdm
from functools import wraps
import pandas as pd
import os
import argparse
import logging

# Root 
logger_name = "__main__"
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
# Argparse
parser = argparse.ArgumentParser(description='')
parser.add_argument('--source', '-C', default="src/사고사망자리스트(10개년)" ,type=str, help=f'Source file directory. (default: "src/사고사망자리스트(10개년)")')
parser.add_argument('--tqdm', default=True, type=bool, help='TQDM (default: True)')
args = parser.parse_args()
# set tqdm pandas
if args.tqdm:
    tqdm.pandas()
# @lru_cache(maxsize=128)
def get_df(root_dir : str) -> pd.DataFrame:
    for idx, xls in enumerate(tqdm(File.get_xlsx(root_dir), desc=f"Reading excel files in {root_dir}")):
        if idx <= 0:
            df : pd.DataFrame = File.readfile(os.path.join(root_dir, xls))
        else:
            df : pd.DataFrame = pd.concat([df, File.readfile(os.path.join(root_dir, xls))], ignore_index=True)
    return df

def process_file(func):
    @wraps(func)
    def wrapper(file_path: str, *args, **kwargs):
        df = File.readfile(file_path)
        result_df = func(df, *args, **kwargs)
        output_path = file_path.replace('src', 'output').replace('.xlsx', '_classified.xlsx')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        result_df.to_excel(output_path, index=False)
        return output_path
    return wrapper

@process_file
def classify_cases_in_df(df: pd.DataFrame) -> pd.DataFrame:
    df['작업유형'] = df['재해개요'].progress_apply(classify_case)
    return df

def get_xlsx_files(root_dir: str):
    return [os.path.join(root_dir, f) for f in os.listdir(root_dir) if f.endswith('.xlsx')]

# main
def main() -> None:
    for file in tqdm(get_xlsx_files(args.source), desc="Processing files"):
        output_file = classify_cases_in_df(file)
        logger.info(f"Processed and saved: {output_file}")

# Main
if __name__ == '__main__':
    main()
