import math


def divide_list(seq, num):
    size = int(math.ceil(float(len(seq)) / num))

    return  [seq[i * size:(i + 1) * size] for i in range(num)]
