import math
from multiprocessing import Pool
from typing import List


def merge(*args):
    left, right = args[0] if len(args) == 1 else args
    left_length, right_length = len(left), len(right)
    left_index, right_index = 0, 0
    merged = []
    while left_index < left_length and right_index < right_length:
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    if left_index == left_length:
        merged.extend(right[right_index:])
    else:
        merged.extend(left[left_index:])
    return merged


def merge_sort(data):
    length = len(data)
    if length <= 1:
        return data
    middle = length // 2
    left = merge_sort(data[:middle])
    right = merge_sort(data[middle:])
    return merge(left, right)


def merge_sort_parallel(
    array: List[int],
    number_of_workers: int = 1
) -> List[int]:
    
    assert number_of_workers > 0

    pool = Pool(processes=number_of_workers)
    size = int(math.ceil(float(len(array)) / number_of_workers))

    array = [array[i * size:(i + 1) * size] for i in range(number_of_workers)]
    array = pool.map(merge_sort, array)

    while len(array) > 1:
        extra = array.pop() if len(array) % 2 == 1 else None

        array = [(array[i], array[i + 1]) for i in range(0, len(array), 2)]
        array = pool.map(merge, array) + ([extra] if extra else [])

    pool.close()
    pool.join()

    return array[0]
