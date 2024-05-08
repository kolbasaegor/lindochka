import time

from typing import List


def search_passwords_sequential(
    passwords_to_search: List[str],
    passwords: List[dict[str, str]]
) -> List[tuple[str, str]]:

    result = []

    start = time.perf_counter()

    for hashed_password in passwords_to_search:
        for item in passwords:
            if hashed_password == item['hashed_password']:
                result.append((item['hashed_password'], item['password']))
                break

    end = time.perf_counter()

    return result, end - start
