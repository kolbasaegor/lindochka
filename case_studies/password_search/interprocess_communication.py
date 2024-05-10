from multiprocessing import Pool, Manager
from multiprocessing.managers import ListProxy
from typing import List

from utils import divide_list


def worker(
    target_passwords: List[str],
    all_passwords: List[dict[str, str]],
    result: ListProxy
) -> None:
    
    for password in target_passwords:
        for item in all_passwords:
            if password == item['hashed_password']:
                result.append((item['hashed_password'], item['password']))
                break


def search_passwords_parallel(
    passwords_to_search: List[str],
    passwords: List[dict[str, str]],
    number_of_workers: int = 1
) -> List[tuple[str, str]]:
    
    assert number_of_workers > 0
    
    manager = Manager()
    pool = Pool(processes=number_of_workers)

    shared_result = manager.list()
    parts = divide_list(passwords_to_search, number_of_workers)
    args = [(part, passwords, shared_result) for part in parts]
    
    pool.starmap(worker, args)

    pool.close()
    pool.join()

    return list(shared_result)
