import time
import random

from utils import merge_sort

random.seed(52)

array_size = 10000000

array = [random.randint(-1000, 1000) for _ in range(array_size)]

# --------------------------------------------------------------------

if __name__ == "__main__":

    print(f'{array_size=}\n')

    print('[start]')
    start = time.perf_counter()

    result = merge_sort(array)

    end = time.perf_counter()
    print('[end]')

    # print(f'{result=}')
    print('sorting time =', end - start, 's')
