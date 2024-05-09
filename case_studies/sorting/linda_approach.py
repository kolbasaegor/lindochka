import operator
import lindypy
from typing import List

from utils import merge, merge_sort, divide_list


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


def merge_sort_linda(
    array: List[int],
    number_of_workers: int = 1
) -> List[int]:
    
    assert number_of_workers > 0
    
    parts = divide_list(array, number_of_workers)
    data = []

    with lindypy.tuplespace() as ts:
        
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

    return data
