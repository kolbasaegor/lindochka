import lindypy
import multiprocessing
import time

from typing import List

from utils import divide_list


def worker(ts, part_of_passwords):
    for password in part_of_passwords:
        ts.out(('hash_pair', password['hashed_password'], password['password']))

    while True:
        task = ts.inp(('search_task', str, 'not_processed'))

        answer = ts.rd(('hash_pair', task[1], str))

        ts.out(('found_password', answer[1], answer[2]))


def search_password_linda(
    passwords_to_search: List[str],
    passwords: List[dict[str, str]],
    number_of_workers: int = -1
) -> List[tuple[str, str]]:
    
    number_of_workers = number_of_workers \
    if number_of_workers > 0 else multiprocessing.cpu_count()

    result = []

    parts = divide_list(passwords, number_of_workers)

    with lindypy.tuplespace() as ts:

        start = time.perf_counter()

        for i in range(len(parts)):
            ts.eval(worker, parts[i])

        for hashed_password in passwords_to_search:
            ts.out(('search_task', hashed_password, 'not_processed'))

        for _ in range(len(passwords_to_search)):
            res = ts.inp(('found_password', str, str))
            result.append((res[1], res[2]))

        end = time.perf_counter()

    return result, end - start
