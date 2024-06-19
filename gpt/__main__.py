# Internal Modules
from ..config.api_keys import openai_api_key
from ..utils.myos import File
# External Modules
# from functools import lru_cache
from tqdm import tqdm
import pandas as pd
import os
import argparse
import logging

# Root 
logger_name = "gpt"
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
# main
def main() -> None:
    df : pd.DataFrame = get_df(args.source)

# Main
if __name__ == '__main__':
    main()
