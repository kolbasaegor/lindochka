import math
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
    size = int(math.ceil(float(len(seq)) / num))

    return  [seq[i * size:(i + 1) * size] for i in range(num)]