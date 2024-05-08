import random
import time

from utils import merge_sort
from linda_approach import merge_sort_linda


random.seed(52)

array_size = 1000000
array = [random.randint(-1000, 1000) for _ in range(array_size)]

if __name__ == "__main__":

    start = time.perf_counter()
    merge_sort(array)
    end = time.perf_counter()
    print("t1 =", end - start, "s")

    _, time_ = merge_sort_linda(array, number_of_workers=4)
    print("t2 =", time_, "s")