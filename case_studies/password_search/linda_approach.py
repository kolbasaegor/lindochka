import time
import lindypy

from utils import from_csv_to_dict, get_random_passwords, divide_list

number_of_passwords = 100000
number_of_passwords_to_search = 1000
number_of_workers = 2

db = from_csv_to_dict(f'data/hashed_passwords{number_of_passwords}.csv')

passwords_to_search = get_random_passwords(
    db=db,
    num=number_of_passwords_to_search,
    seed=52
)

result = []

# --------------------------------------------------------------------

def worker(ts, part_of_passwords):
    for password in part_of_passwords:
        ts.out(('hash_pair', password['hashed_password'], password['password']))

    while True:
        task = ts.inp(('search_task', str, 'not_processed'))

        answer = ts.rd(('hash_pair', task[1], str))

        ts.out(('found_password', answer[1], answer[2]))


if __name__ == "__main__":
    print(f'{number_of_passwords=}\n{number_of_passwords_to_search=}\n{number_of_workers=}\n')
    
    parts = divide_list(db, number_of_workers)

    with lindypy.tuplespace() as ts:

        print('[start]')
        start = time.perf_counter()

        for i in range(len(parts)):
            ts.eval(worker, parts[i])

        for hashed_password in passwords_to_search:
            ts.out(('search_task', hashed_password, 'not_processed'))

        for _ in range(len(passwords_to_search)):
            res = ts.inp(('found_password', str, str))
            result.append((res[1], res[2]))

        end = time.perf_counter()
        print('[end]')

    print('Search time =', end - start, 's')
