import random
import time

from utils import merge_sort
from linda_approach import merge_sort_linda
from interprocess_communication import merge_sort_parallel


random.seed(52)

array_size = 10000 # на измене

array = [random.randint(-1000, 1000) for _ in range(array_size)]

if __name__ == "__main__":
    print('Array size:', array_size)
    print('----------------------------------')

    start = time.perf_counter()
    merge_sort_linda(array, number_of_workers=4)
    end = time.perf_counter()
    print("linda:", end - start, "s")

    start = time.perf_counter()
    merge_sort_parallel(array, number_of_workers=4)
    end = time.perf_counter()
    print("interprocess communication:", end - start, "s")

    start = time.perf_counter()
    merge_sort(array)
    end = time.perf_counter()
    print("sequential:", end - start, "s")
