import os
import operator
import time
import random
import lindypy

from utils import merge, merge_sort, divide_list

random.seed(52)

array_size = 10000000
number_of_workers = 4

array = [random.randint(-1000, 1000) for _ in range(array_size)]

# --------------------------------------------------------------------

def worker(ts, initial_index, inital_array):
    sorted_array = merge_sort(inital_array)
    ts.out(('sorted', initial_index, iter(sorted_array)))

    while True:
        merge_task = ts.inp(('merge', int, tuple))

        ts.out((
            'merged',
            merge_task[1],
            iter(merge(merge_task[2][0], merge_task[2][1], compare=operator.lt))
        ))


if __name__ == "__main__":

    parts = divide_list(array, number_of_workers)
    data = []
    
    with lindypy.tuplespace() as ts:
        
        start = time.perf_counter()

        for i in range(number_of_workers):
            ts.eval(worker, i, parts[i])

        data = [
            list(ts.inp(('sorted', i, object))[2]) for i in range(number_of_workers)
        ]

        while len(data) > 1:
            extra = data.pop() if len(data) % 2 == 1 else None

            for i in range(0, len(data), 2):
                ts.out(('merge', i // 2, (data[i], data[i+1])))

            data = [
                list(ts.inp(('merged', i // 2, object))[2]) for i in range(0, len(data), 2)
            ] + ([extra] if extra else [])            

        end = time.perf_counter()

    # print('result:', data[0])
    print(f'{end - start} s')

