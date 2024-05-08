import pandas as pd
import random

from typing import List


def from_csv_to_dict(filename: str) -> List[dict[str, str]]:
    data = pd.read_csv(filename)

    return data.to_dict(orient='records')


def get_random_passwords(db: List[dict[str, str]], num: int) -> List[str]:
    if num < 1 or len(db) < num:
        return []
    
    return [item['hashed_password'] for item in random.choices(db, k=num)]


def divide_list(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out
         