import time
import random
import sys
from multiprocessing import cpu_count

from utils import from_csv_to_dict, get_random_passwords

from sequential_approach import search_passwords_sequential
from linda_approach import search_passwords_linda
from interprocess_communication import search_passwords_parallel


random.seed(52)

number_of_passwords = int(sys.argv[1])
number_of_passwords_to_search = int(sys.argv[2])

if (len(sys.argv) == 4):
    number_of_workers = int(sys.argv[3])
else:
    number_of_workers = cpu_count()

db = from_csv_to_dict(f'data/hashed_passwords{number_of_passwords}.csv')

passwords_to_search = get_random_passwords(
    db=db,
    num=number_of_passwords_to_search,
)

if __name__ == "__main__":
    print('Number of passwords:', number_of_passwords)
    print('Number of passwords to search:', number_of_passwords_to_search)
    print('----------------------------------')

    start = time.perf_counter()
    search_passwords_linda(passwords_to_search, db, number_of_workers=number_of_workers)
    end = time.perf_counter()
    print("linda:", end - start, "s")

    start = time.perf_counter()
    search_passwords_parallel(passwords_to_search, db, number_of_workers=number_of_workers)
    end = time.perf_counter()
    print("interprocess communication:", end - start, "s")

    start = time.perf_counter()
    search_passwords_sequential(passwords_to_search, db)
    end = time.perf_counter()
    print("sequential:", end - start, "s")
