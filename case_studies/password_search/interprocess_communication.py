import multiprocessing
from typing import List


def search_password_linda(
    passwords_to_search: List[str],
    passwords: List[dict[str, str]],
    number_of_workers: int = 1
) -> List[tuple[str, str]]:
    
    assert number_of_workers > 0

    pool = multiprocessing.Pool(processes=number_of_workers)

    
