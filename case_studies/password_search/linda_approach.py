import lindypy

from typing import List


def worker(ts, all_passwords):
    while True:
        task = ts.inp(('search_task', str))

        for item in all_passwords:
            if task[1] == item['hashed_password']:
                ts.out(('found_password', item['hashed_password'], item['password']))
                break


def search_passwords_linda(
    passwords_to_search: List[str],
    passwords: List[dict[str, str]],
    number_of_workers: int = 1
) -> List[tuple[str, str]]:
    
    assert number_of_workers > 0

    result = []

    with lindypy.tuplespace() as ts:

        for _ in range(number_of_workers):
            ts.eval(worker, passwords)

        for hashed_password in passwords_to_search:
            ts.out(('search_task', hashed_password))

        for _ in range(len(passwords_to_search)):
            res = ts.inp(('found_password', str, str))
            result.append((res[1], res[2]))

    return result
